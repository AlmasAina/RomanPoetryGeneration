import streamlit as st
import os
import backend

st.set_page_config(page_title="VerseCraft: Poetry Generator", layout="wide")

# 🎨 **Custom Styling**
st.markdown("""
    <style>
    body {
        background-color: #87CEEB; /* Sky Blue Background */
        font-family: 'Arial', sans-serif;
        color: #333333; /* Dark Grey Text for readability */
    }
    .title {
        text-align: center;
        font-size: 48px;
        color: #4169E1; /* Royal Blue for Title */
        margin-bottom: 40px;
    }
    .stTextInput, .stSlider, .stSelectbox, .stButton > button, .stTextArea textarea {
        background-color: transparent;
        border: none;
        font-size: 16px;
        margin-bottom: 20px;
        padding: 10px;
        box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.1);
        border-radius: 8px;
    }
    .stTextInput input, .stTextArea textarea {
        font-family: 'Arial', sans-serif;
        background-color: #FFFFFF; /* White background for input */
    }
    .stButton > button {
        background-color: #4169E1; /* Royal Blue */
        color: white;
        font-size: 18px;
        padding: 10px 20px;
        border-radius: 8px;
        cursor: pointer;
        transition: background-color 0.3s;
        border: none;
    }
    .stButton > button:hover {
        background-color: #3b5b9d; /* Darker shade of blue on hover */
    }
    .stAlert {
        background-color: #f0f8ff; /* Light Blue for alerts */
        color: #4169E1; /* Royal Blue text */
        border-left: 5px solid #4169E1; /* Royal Blue border */
    }
    .stSuccess {
        background-color: #e9f5e9; /* Light Green Success */
        color: #388E3C; /* Green text */
        border-left: 5px solid #388E3C; /* Green border */
    }
    .stWarning {
        background-color: #fff3cd; /* Light Yellow for Warnings */
        color: #8a6d3b; /* Dark Yellow text */
        border-left: 5px solid #8a6d3b; /* Dark Yellow border */
    }
    .stSlider .stSlider__range {
        background-color: #4169E1; /* Royal Blue slider */
    }
    </style>
""", unsafe_allow_html=True)

# ✅ **Title**
st.markdown("<h1 class='title'>VerseCraft: Poetry Generator</h1>", unsafe_allow_html=True)

# ✅ **File Upload**
uploaded_file = st.file_uploader("Upload your poetry dataset (CSV)", type=["csv"])

# ✅ **File Upload Handling**
if uploaded_file:
    file_path = os.path.join("data", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"✅ File '{uploaded_file.name}' uploaded successfully!")

    # ✅ **Data Preprocessing - Only happens once**
    if 'preprocessed' not in st.session_state:
        if st.button("Preprocess Text"):
            vocab_size, tokenizer = backend.preprocess_text(file_path, sequence_length=10)
            st.session_state.preprocessed = True
            st.session_state.vocab_size = vocab_size
            st.session_state.tokenizer = tokenizer
            st.success("✅ Text Preprocessed!")

# ✅ **Model Hyperparameters**
st.sidebar.header("📌 Model Hyperparameters")
embedding_dim = st.sidebar.slider("Embedding Dimension", 50, 300, 100)
lstm_units = st.sidebar.slider("LSTM Units", 50, 300, 150)
batch_size = st.sidebar.selectbox("Batch Size", [32, 64, 128, 256], index=2)
epochs = st.sidebar.slider("Epochs", 10, 100, 50)
learning_rate = st.sidebar.slider("Learning Rate", 0.0001, 0.01, 0.001, format="%.4f")

# ✅ **Train Model (Persistent training check)**
if 'preprocessed' in st.session_state:
    if 'trained' not in st.session_state:
        if st.button("Train Model"):
            with st.spinner("Training in Progress..."):
                backend.train_model(embedding_dim, lstm_units, batch_size, epochs, learning_rate, sequence_length=10)
            st.session_state.trained = True
            st.success("✅ Model Training Complete!")
    else:
        st.success("Model already trained!")
else:
    st.warning("Please preprocess the text first!")

# ✅ **Poetry Generation (Only shown after model is trained)**
if 'trained' in st.session_state:
    # Generate Poetry Section
    st.subheader("📝 Generate Poetry")
    seed_text = st.text_input("Enter Seed Text:", "mujh se pehli si mohabbat")
    next_words = st.slider("Number of Words to Generate:", 10, 100, 50)
    if st.button("Generate Poetry"):
        generated_poetry = backend.generate_poetry(seed_text, next_words, sequence_length=10, tokenizer=st.session_state.tokenizer)
        st.text_area("Generated Poetry:", generated_poetry, height=200)

    # Generate Poetry from Saved Model Section
    st.subheader("📝 Generate Poetry from Saved Model")
    seed_text_saved = st.text_input("Enter Seed Text (for saved model):", "hasina daniya ky laab")
    next_words_saved = st.slider("Number of Words to Generate (Saved Model):", 10, 100, 50)
    if st.button("Generate Poetry from Saved Model"):
        generated_poetry_saved = backend.generate_poetry(seed_text_saved, next_words_saved, sequence_length=10, tokenizer=st.session_state.tokenizer)
        st.text_area("Generated Poetry (Saved Model):", generated_poetry_saved, height=200)
else:
    st.warning("Please train the model first!")
