import streamlit as st
import os
import backend

st.set_page_config(page_title="VerseCraft: Poetry Generator", layout="centered")

# 🎨 **Custom Styling (Gorgeous, Elegant, and Interactive Design)**
st.markdown("""
    <style>
    /* Animated Background Gradient with glowing effect */
    body {
        background: linear-gradient(45deg, #ff9a8b, #ff6a88, #d17c85, #6a3dff); /* Vibrant Gradient */
        background-size: 400% 400%;
        animation: gradientAnimation 20s ease infinite;
        font-family: 'Poppins', sans-serif;
        color: #ffffff;
        margin: 0;
        padding: 0;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        text-align: center;
        background-attachment: fixed;
    }

    /* Keyframe animation for the gradient background */
    @keyframes gradientAnimation {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Title Styling (Gorgeous and elegant font) */
    .title {
        font-size: 70px;
        color: #ffffff;
        font-weight: bold;
        margin-bottom: 40px;
        text-shadow: 6px 6px 15px rgba(0, 0, 0, 0.6);
        font-family: 'Playfair Display', serif;
    }

    /* Content Box Styling (Smooth, elegant card) */
    .content {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        padding: 40px;
        border-radius: 20px;
        background: rgba(255, 255, 255, 0.8); /* Soft transparent white background */
        box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.3);
        transition: all 0.4s ease;
        width: 85%;
        max-width: 600px;
    }

    .content:hover {
        box-shadow: 0px 15px 35px rgba(0, 0, 0, 0.5); /* Hover effect to enhance the feel */
        transform: scale(1.02);
    }

    /* Styling for input fields, sliders, and buttons */
    .stTextInput, .stSlider, .stSelectbox, .stButton > button, .stTextArea textarea {
        background-color: #ffffff;
        border: 2px solid #ff6a88; /* Soft Pink Border */
        font-size: 18px;
        margin: 10px 0;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0px 6px 12px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        width: 80%;
        max-width: 500px;
    }

    /* Focus effect for inputs */
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #6a3dff; /* Elegant Purple */
        box-shadow: 0px 0px 15px rgba(106, 61, 255, 0.5);
    }

    /* Hover effect for buttons */
    .stButton > button {
        background-color: #ff6a88; /* Soft Pink */
        color: white;
        font-size: 22px;
        padding: 18px 24px;
        border-radius: 12px;
        cursor: pointer;
        transition: transform 0.3s ease, background-color 0.3s ease;
        border: none;
    }

    .stButton > button:hover {
        background-color: #d17c85; /* Deep Peach Hover */
        transform: scale(1.1); /* Subtle hover animation */
    }

    /* Text area for generated poetry */
    .stTextArea textarea {
        font-family: 'Poppins', sans-serif;
        font-size: 18px;
        color: #333333;
        background-color: #ffffff;
        border: 2px solid #ff6a88;
        border-radius: 10px;
        padding: 15px;
        transition: all 0.3s ease;
    }

    /* Alert, success, and warning messages */
    .stAlert {
        background-color: #fdf1c7;
        color: #333333;
        border-left: 5px solid #ff9800;
        padding: 15px;
    }

    .stSuccess {
        background-color: #66bb6a;
        color: #ffffff;
        border-left: 5px solid #388e3c;
        padding: 15px;
    }

    .stWarning {
        background-color: #ffeb3b;
        color: #000000;
        border-left: 5px solid #f57c00;
        padding: 15px;
    }

    /* Slider with glowing effect */
    .stSlider .stSlider__range {
        background-color: #ff6a88;
        height: 12px;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# ✅ **Title**
st.markdown("<h1 class='title'>VerseCraft: Poetry Generator</h1>", unsafe_allow_html=True)

# ✅ **Centered Content Container**
# st.markdown("<div class='content'>", unsafe_allow_html=True)

# ✅ **Load Tokenizer**
if 'tokenizer' not in st.session_state:
    st.session_state.tokenizer = backend.load_tokenizer()

# ✅ **Poetry Generation (Using Pre-trained Model)**
st.subheader("📝 Enter a Seed Text and Generate Your Poetry")

seed_text = st.text_input("Seed Text:", "mujh se pehli si mohabbat", key="seed_text", placeholder="Start your poetic journey here...")
if st.button("Generate Poetry", key="generate_poetry"):
    generated_poetry = backend.generate_poetry(seed_text, sequence_length=10, tokenizer=st.session_state.tokenizer)
    st.text_area("Generated Poetry:", generated_poetry, height=300, max_chars=1000)

# ✅ **End of content container**
st.markdown("</div>", unsafe_allow_html=True)
