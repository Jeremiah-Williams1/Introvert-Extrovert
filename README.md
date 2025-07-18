# Introvert vs Extrovert Personality Classifier 

This project is a machine learning pipeline that classifies whether a person is an **introvert** or an **extrovert** based on some behavioral features.

The workflow includes:
- Training with `scikit-learn` in a Jupyter Notebook
- Model + preprocessing serialization
- API built with FastAPI
- Docker container for deployment

---

## 🔍 Project Overview

| Stage | Details |
|-------|---------|
| **Modeling** | Trained in a `.ipynb` notebook using `scikit-learn` |
| **Data** | Personality trait data  |
| **Preprocessing** | Encoded inputs (saved as pickle), data validation with pydantic |
| **Model** | XgbClassifier |
| **Serving** | FastAPI + Uvicorn |
| **Deployment** | Docker containerized |

---

## 🧠 How It Works

1. The model takes in personality-related inputs.
2. Preprocessing pipeline transforms input to model-ready format(data validaion).
3. FastAPI receives JSON input, applies preprocessing + prediction.
4. A JSON response returns the predicted personality type.

---