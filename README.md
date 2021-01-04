# Hostile Post Detection in Hindi

Code for reproducing Team 'Albatross' result in the competition https://competitions.codalab.org/competitions/26654.

## Best Results
In the `src/best_results/` we have stored the best results that we were getting.

Go to `src/best_results/`:
1. Run `Combining_Results_BinaryRelevance.ipynb'
2. Run `Evaluation_Script.py'

## System Architecture
 ![Layered Architecture Inference](/docs/LayeredArchitectureInference.png)
 
## Data Preprocessing
In the `src` directory, run `data_preprocessing.py`. This script processes the raw data to extract hashtags, emojis, mentions, etc.

The processed data files are available in `data/processed` directory.

## Running the Models

Use `train.csv`, `test.csv`, `val.csv` present in the `data/processed/` directory for all further operations.

Use `hate_words.csv` present in `src/best_model/` wherever required below.

In `src/best_model/` directory, run the models in the following sequence:

1. Run `Non_Hostile_Model.ipynb`.
2. Run `Fake_Model.ipynb`.
3. Run `Hate_Model.ipynb`.
4. Run `Offensive_Model.ipynb`.
5. Run `Defamation_Model.ipynb`.
6. Run `Combining_Results_BinaryRelevance.ipynb`.
7. Run `Evaluation_Script.py`.

## Team Members
1. Varad Bhatnagar
2. Prince Kumar
3. Sairam Moghili
