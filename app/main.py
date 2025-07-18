from fastapi import FastAPI
from predict import make_prediction
from pydantic_model import features
app = FastAPI()


@app.get('/')
def display():
    return {'Message': 'Welcome to Personality Prediction',
            'Goto': '/predict root for prediction'
            }

@app.post('/predict')
def predict_class(input_data:features):
    result = make_prediction(input_data.dict())
    # request inputs from users
    if result == 1:
        return 'Introvert'
    else:
        return 'Extrovet'


# set a variable port and host 
# then create a dockerfile for these 
# run the docerfile and upload the container to the hub