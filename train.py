"""
Author: Amisha & Aditya
Date: 2024-05-30
"""
import os
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow.keras.layers import Embedding, LSTM, Dense, Bidirectional, Dropout, TimeDistributed, Input
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.utils import to_categorical

# Import the preprocessing function
from app.preprocessing import load_and_preprocess_data

# Define paths
data_path = os.path.join(os.path.dirname(__file__), '.', 'data', 'config.json')
csv_output_path = os.path.join(os.path.dirname(__file__), '.', 'data', 'data.csv')

# Load and preprocess the data
df = load_and_preprocess_data(data_path)

# Save preprocessed DataFrame to CSV
df.to_csv(csv_output_path, sep='|', index=False)

# Tokenize and pad sequences
tokenizer = Tokenizer()
tokenizer.fit_on_texts(df['question'].tolist() + df['answer'].tolist())
X_question = tokenizer.texts_to_sequences(df['question'])
X_answer = tokenizer.texts_to_sequences(df['answer'])

max_length = max(max(len(seq) for seq in X_question), max(len(seq) for seq in X_answer))

X_question = pad_sequences(X_question, maxlen=max_length, padding='post')
X_answer = pad_sequences(X_answer, maxlen=max_length, padding='post')

# Convert the scores to a NumPy array and ensure the correct type
y = np.array(df['score']).astype(float)

# Split the data
X_train_q, X_test_q, X_train_a, X_test_a, y_train, y_test = train_test_split(
    X_question, X_answer, y, test_size=0.2, random_state=42
)

# One-hot encode the target sequences for the QA model
y_train_a = np.array([to_categorical(seq, num_classes=len(tokenizer.word_index) + 1) for seq in X_train_a])
y_test_a = np.array([to_categorical(seq, num_classes=len(tokenizer.word_index) + 1) for seq in X_test_a])

# Define the RNN model for answer rating
answer_model = Sequential([
    Embedding(input_dim=len(tokenizer.word_index) + 1, output_dim=128, input_length=max_length),
    Bidirectional(LSTM(64, return_sequences=True)),
    Dropout(0.5),
    Bidirectional(LSTM(32)),
    Dense(1, activation='linear')
])

answer_model.compile(optimizer='adam', loss='mean_squared_error')
answer_model.fit(X_train_a, y_train, epochs=10, batch_size=32, validation_split=0.2)

# Define the RNN model for question-answer matching
inputs = Input(shape=(max_length,))
x = Embedding(input_dim=len(tokenizer.word_index) + 1, output_dim=128, input_length=max_length)(inputs)
x = Bidirectional(LSTM(64, return_sequences=True))(x)
x = Dropout(0.5)(x)
x = Bidirectional(LSTM(32, return_sequences=True))(x)
outputs = TimeDistributed(Dense(len(tokenizer.word_index) + 1, activation='softmax'))(x)

qa_model = Model(inputs, outputs)
qa_model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
qa_model.fit(X_train_q, y_train_a, epochs=10, batch_size=32, validation_split=0.2)

# Save the models in the native Keras format
model_dir = os.path.join(os.path.dirname(__file__), '.', 'models')
os.makedirs(model_dir, exist_ok=True)

# Save the tokenizer
tokenizer_path = os.path.join(model_dir, 'tokenizer.pkl')
with open(tokenizer_path, 'wb') as f:
    joblib.dump(tokenizer, f)

# Save the models
answer_model_path = os.path.join(model_dir, 'answer_model.keras')
qa_model_path = os.path.join(model_dir, 'qa_model.keras')

answer_model.save(answer_model_path)
qa_model.save(qa_model_path)
