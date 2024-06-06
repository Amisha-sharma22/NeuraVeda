import joblib
from app.preprocessing import preprocess_text

# Load models
vectorizer = joblib.load('models/vectorizer.pkl')
rating_model = joblib.load('models/rating_model.pkl')
pipeline = joblib.load('models/pipeline.pkl')

def rate_answer(answer):
    answer_preprocessed = preprocess_text(answer)
    X_new = vectorizer.transform([answer_preprocessed])
    rating = rating_model.predict(X_new)[0]
    return rating

def get_bot_response(user_question):
    user_question_preprocessed = preprocess_text(user_question)
    response = pipeline.predict([user_question_preprocessed])[0]
    return response