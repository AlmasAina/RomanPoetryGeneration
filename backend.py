import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle

# ✅ Generate Poetry (using pre-trained model)
def generate_poetry(seed_text, sequence_length, tokenizer):
    model = tf.keras.models.load_model("lstm_poetry_model.h5")  # Load the pre-trained model
    generated_text = seed_text

    next_words = 50  # Fixed number of words to generate
    temperature = 1.0  # Fixed temperature for prediction
    words_per_line = 7  # Fixed number of words per line

    for i in range(next_words):
        token_list = tokenizer.texts_to_sequences([generated_text])[0]
        token_list = pad_sequences([token_list], maxlen=sequence_length, padding='pre')

        predicted = model.predict(token_list, verbose=0)[0]

        # Apply temperature
        predicted = np.asarray(predicted).astype('float64')
        predicted = np.log(predicted + 1e-7) / temperature
        predicted = np.exp(predicted) / np.sum(np.exp(predicted))  # Normalize

        predicted_word_index = np.random.choice(len(predicted), p=predicted)  # Select word based on temperature distribution

        for word, index in tokenizer.word_index.items():
            if index == predicted_word_index:
                generated_text += " " + word
                break

        # Add a new line after every `words_per_line` words
        if (i + 1) % words_per_line == 0:
            generated_text += "\n"

    return generated_text

# ✅ Load the tokenizer from the saved file
def load_tokenizer():
    with open("tokenizer.pkl", "rb") as f:
        tokenizer = pickle.load(f)
    return tokenizer
