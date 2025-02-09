import os
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.optimizers import Adam

# ✅ Preprocess the Text
def preprocess_text(file_path, sequence_length):
    df = pd.read_csv(file_path)

    # Combine all poetry into a single text
    all_poetry = " ".join(df["Poetry"].astype(str).tolist()).lower()

    # Remove unnecessary characters
    import re
    cleaned_text = re.sub(r"[^a-zA-Z0-9\s]", "", all_poetry)
    cleaned_text = re.sub(r"\s+", " ", cleaned_text).strip()

    # Tokenize
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts([cleaned_text])
    sequence_data = tokenizer.texts_to_sequences([cleaned_text])[0]

    # Vocabulary size
    vocab_size = len(tokenizer.word_index) + 1

    # Generate sequences
    sequences = []
    for i in range(sequence_length, len(sequence_data)):
        seq = sequence_data[i-sequence_length:i+1]
        sequences.append(seq)

    sequences = np.array(sequences)

    # Save sequences
    np.savetxt("preprocessed_sequences.csv", sequences, delimiter=",")
    return vocab_size, tokenizer

# ✅ Split the Data
def split_data(sequence_length):
    sequences = np.loadtxt("preprocessed_sequences.csv", delimiter=",")
    X, y = sequences[:, :-1], sequences[:, -1]

    # Train-Validation-Test Split
    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.2, random_state=42)
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

    # Save
    pd.DataFrame(np.column_stack([X_train, y_train])).to_csv("train_data.csv", index=False, header=False)
    pd.DataFrame(np.column_stack([X_val, y_val])).to_csv("val_data.csv", index=False, header=False)
    pd.DataFrame(np.column_stack([X_test, y_test])).to_csv("test_data.csv", index=False, header=False)

    return X_train, y_train, X_val, y_val, X_test, y_test
def train_model(embedding_dim, lstm_units, batch_size, epochs, learning_rate, sequence_length):
    # Load and verify data
    train_data = pd.read_csv("train_data.csv", header=None)
    val_data = pd.read_csv("val_data.csv", header=None)

    # Convert to numpy arrays and ensure correct data types
    X_train = train_data.iloc[:, :-1].values
    y_train = train_data.iloc[:, -1].values
    X_val = val_data.iloc[:, :-1].values
    y_val = val_data.iloc[:, -1].values

    # Ensure that X_train and y_train are of correct type and shape
    X_train = np.array(X_train, dtype=np.int32)
    y_train = np.array(y_train, dtype=np.int32)
    X_val = np.array(X_val, dtype=np.int32)
    y_val = np.array(y_val, dtype=np.int32)

    # Check if shapes are correct
    print(f"X_train shape: {X_train.shape}")
    print(f"y_train shape: {y_train.shape}")
    print(f"X_val shape: {X_val.shape}")
    print(f"y_val shape: {y_val.shape}")

    # Define the model
    model = Sequential([
        # Embedding(input_dim=np.max(X_train)+1, output_dim=embedding_dim, input_length=sequence_length),
        Embedding(input_dim=np.max(X_train)+1, output_dim=embedding_dim),

        LSTM(lstm_units, return_sequences=True),
        LSTM(lstm_units),
        Dense(lstm_units, activation="relu"),
        Dense(np.max(y_train)+1, activation="softmax")  # Output layer size based on y_train
    ])

    model.compile(loss="sparse_categorical_crossentropy", optimizer=Adam(learning_rate=learning_rate), metrics=["accuracy"])

    # Train the model
    history = model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, validation_data=(X_val, y_val), verbose=1)

    # Save the model
    model.save("lstm_poetry_model.h5")
    return "Model Trained & Saved!"

# ✅ Generate Poetry
# ✅ Generate Poetry with Line Breaks
def generate_poetry(seed_text, next_words, sequence_length, tokenizer, words_per_line=7):
    model = tf.keras.models.load_model("lstm_poetry_model.h5")
    generated_text = seed_text

    for i in range(next_words):
        token_list = tokenizer.texts_to_sequences([generated_text])[0]
        token_list = pad_sequences([token_list], maxlen=sequence_length, padding='pre')

        predicted = model.predict(token_list, verbose=0)
        predicted_word_index = np.argmax(predicted)

        for word, index in tokenizer.word_index.items():
            if index == predicted_word_index:
                generated_text += " " + word
                break

        # Add a new line after every `words_per_line` words
        if (i + 1) % words_per_line == 0:
            generated_text += "\n"

    return generated_text

