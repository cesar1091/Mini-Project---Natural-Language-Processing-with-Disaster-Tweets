from flask import Flask, render_template, request, jsonify
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
from utils.preprocess import clean_text
import os

print("Current working directory:", os.getcwd())

app = Flask(__name__)

# Load the trained model
model = tf.keras.models.load_model(os.getcwd() + '/models/lstm_model.keras')

# Load the tokenizer
with open(os.getcwd() + '/models/tokenizer.pkl', 'rb') as handle:
    tokenizer = pickle.load(handle)

# Define the maximum sequence length (same as used during training)
MAX_SEQUENCE_LENGTH = 50

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Get the tweet from the form
        tweet = request.form['tweet']
        
        # Preprocess the tweet
        cleaned_tweet = clean_text(tweet)
        
        # Tokenize and pad the sequence
        sequence = tokenizer.texts_to_sequences([cleaned_tweet])
        padded_sequence = pad_sequences(sequence, maxlen=MAX_SEQUENCE_LENGTH, truncating='post', padding='post')
        
        # Make prediction
        prediction = model.predict(padded_sequence)[0][0]
        result = 'Disaster' if prediction > 0.5 else 'Non-Disaster'
        
        return jsonify({
            'tweet': tweet,
            'prediction': result,
            'confidence': f"{prediction:.2f}"
        })

if __name__ == '__main__':
    app.run(debug=True)