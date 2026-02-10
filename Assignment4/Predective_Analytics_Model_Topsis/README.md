 Project Overview

This project compares multiple pre-trained NLP models for a text classification task and selects the most suitable one using the TOPSIS (Technique for Order Preference by Similarity to Ideal Solution) decision-making approach.

Instead of relying on a single metric like accuracy, this approach evaluates models using multiple performance measures and ranks them mathematically to determine the optimal choice.

 Methodology

The complete workflow follows these steps:

Data Collection → Model Evaluation → Performance Metrics Calculation → TOPSIS Scoring → Ranking

Collect and preprocess text dataset

Run classification using different pre-trained models

Record evaluation metrics (accuracy, precision, recall, etc.)

Apply TOPSIS to compute scores

Rank models based on closeness to the ideal solution

 Project Details

Dataset Used: stanfordnlp/sst2.csv

Weights: Positive values only (> 0)

Impacts: Benefit (+) or Cost (–) criteria

Outputs Generated: Performance table and visualization graphs

 Objectives

Apply the TOPSIS algorithm using basic mathematical computations

Compare multiple models fairly using several evaluation metrics

Identify the best-performing text classification model

Analyze how modifying weights and impacts affects rankings

 Results
🗃 Input Dataset
<img width="518" height="625" alt="image" src="https://github.com/user-attachments/assets/19497b27-281c-4d5d-89fd-6765b5605743" />
📊 Output Table
<img width="1236" height="489" alt="image" src="https://github.com/user-attachments/assets/86510cf7-7440-41ec-a247-2b0ad23991b6" />
📉 Output Graphs
<img width="789" height="585" alt="image" src="https://github.com/user-attachments/assets/3e3d614d-1e6b-4cab-acce-700d44718403" /> <img width="789" height="588" alt="image" src="https://github.com/user-attachments/assets/d5bb09b8-76d4-4506-855b-cf7086a8244a" />
 Conclusion
 By integrating TOPSIS with model evaluation, this project provides a structured and unbiased way to select the best classifier.
This multi-criteria approach ensures that decisions are not dependent on a single metric, leading to more reliable and balanced model selection.

By integrating TOPSIS with model evaluation, this project provides a structured and unbiased way to select the best classifier.
This multi-criteria approach ensures that decisions are not dependent on a single metric, leading to more reliable and balanced model selection.
