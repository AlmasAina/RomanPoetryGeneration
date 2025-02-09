VerseCraft: Roman Urdu Poetry Generator
=============================================
Overview
--------
VerseCraft is an AI-powered poetry generator that uses an LSTM (Long Short-Term Memory) model to generate Roman Urdu poetry based on a given seed text.
Features
--------
Upload a Dataset: Accepts a CSV file (Roman-Urdu-Poetry.csv) or any file with the same format.
Preprocess Text: Tokenizes, cleans, and prepares the poetry data for training.
Train the Model: Uses an LSTM-based deep learning model to learn the poetry structure.
Generate Poetry: Enter a seed phrase, and the AI will generate poetry word by word.
Line Breaks for Readability: Generates structured poetry with automatic line breaks.
Installation & Setup
-------------------------
1. Install Python & Required Libraries
Make sure you have Python 3.8+ installed. Then, install the required dependencies using:
Bash
pip install -r requirements.txt
2. Clone the Repository
Bash
git clone https://github.com/AlmasAina/RomanPoetryGeneration.git
cd RomanPoetryGeneration
3. Upload the Dataset
Place your poetry dataset inside the project folder. It should be named: Roman-Urdu-Poetry.csv (or any file with the same format).
How to Run
--------------
Start the Poetry Generator App
Bash
streamlit run frontend.py

    This will open a web interface where you can upload a dataset, train the model, and generate poetry.


## Model Training
-----------------

*   **Training Time**: Takes approximately 1 hour depending on the dataset size and system performance.
*   **Accuracy**: Achieves ~42% accuracy, since it's trained on a small chunk of data.


## Generating Poetry
---------------------

*   **Example Input**: `mujh se pehli si mohabbat`
*   **Example Output**:

    ```
mujh se pehli si mohabbat mere mehboob na maang
jo main dekhoon to tujhe dekh ke jeetay hain log
jo tere husn pe martay hain wo jeetay hain log
-------------
The model automatically adds line breaks every 7 words for readability.
-------------
Limitations
--------------
Not a perfect poet: LSTM models struggle with long-term context understanding.
Grammar Issues: Since it's trained only on Roman Urdu, output may have grammatical inconsistencies.
Small Dataset: The accuracy is limited (~42%), but can be improved by training on larger datasets.
Contributing
--------------
If you'd like to improve this project, feel free to fork and submit a pull request.
License
-------
This project is MIT licensed – feel free to modify and use it!
Contact & Support
---------------------
If you need help, reach out via GitHub Issues or contact @AlmasAina.
Happy Poetry Generation!
