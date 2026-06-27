import os
import json
import time
import logging
import redis
from predict import make_prediction
from prometheus_client import CollectorRegistry, Counter, Histogram, push_to_gateway

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

QUEUE_KEY        = "queue:classification"
JOB_TTL          = 3600
PUSHGATEWAY_URL = os.getenv("PUSHGATEWAY_URL", "http://pushgateway:9091")

registry = CollectorRegistry()

jobs_completed = Counter(
    "inference_jobs_completed_total",
    "Total jobs completed by the classification worker",
    ["type", "status"],
    registry=registry
)

inference_duration = Histogram(
    "inference_duration_seconds",
    "Time spent running the ML model",
    ["type"],
    registry=registry
)

def get_redis():
    url = os.environ["REDIS_URL"]
    return redis.from_url(url, decode_responses=True)

def run_model(input_data: dict):
    result = make_prediction(input_data)
    return {"prediction": result.tolist()}

def process_job(r: redis.Redis, job: dict):
    job_id   = job["id"]
    job_key  = f"job:{job_id}"
    job_type = job.get("type", "classification")

    job["status"]     = "processing"
    job["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    r.set(job_key, json.dumps(job), ex=JOB_TTL)
    log.info(f"processing job {job_id}")

    start = time.time()
    try:
        result = run_model(job["input"])
        job["status"] = "completed"
        job["result"] = result
        job["error"]  = ""
    except Exception as e:
        log.error(f"inference failed for {job_id}: {e}")
        job["status"] = "failed"
        job["error"]  = str(e)
    finally:
        duration = time.time() - start
        inference_duration.labels(type=job_type).observe(duration)
        jobs_completed.labels(type=job_type, status=job["status"]).inc()
        try:
            push_to_gateway(PUSHGATEWAY_URL, job="classification-worker", registry=registry)
        except Exception as e:
            log.warning(f"failed to push metrics: {e}")

    job["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    r.set(job_key, json.dumps(job), ex=JOB_TTL)
    log.info(f"job {job_id} → {job['status']}")

def main():
    r = get_redis()
    log.info("classification worker started, polling queue...")

    while True:
        result = r.brpop(QUEUE_KEY, timeout=5)
        if result is None:
            continue

        _, raw = result
        job = json.loads(raw)
        process_job(r, job)

if __name__ == "__main__":
    main()