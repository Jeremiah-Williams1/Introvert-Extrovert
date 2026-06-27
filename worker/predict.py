import joblib
import numpy as np

le_stage = joblib.load('Stage_fear_le.pkl')
le_personality = joblib.load('Personality_le.pkl')
model = joblib.load('model.pkl')

def preprocess_input(data: dict):
    stage_encoder = le_stage.transform([data['Stage_fear']])[0]
    # personality_encoder = le_personality.transform([data['Personality']])[0]

    features = [
        data['Time_spent_Alone'],
        data['Social_event_attendance'],
        data['Going_outside'],
        data['Friends_circle_size'],
        data['Post_frequency'],
        # personality_encoder,
        stage_encoder
    ]
    return np.array(features).reshape(1, -1)


def make_prediction(data: dict):

    preprocessed = preprocess_input(data)
    pred = model.predict(preprocessed)

    return pred
