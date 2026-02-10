# Synthetic Data Generation Through Simulation-Based Modeling

## Project Overview
This project explores the application of discrete-event simulation for generating synthetic datasets, followed by comprehensive machine learning model evaluation. The methodology demonstrates how simulation frameworks can create realistic data scenarios for algorithmic testing and comparison.

## Implementation Pipeline

The project follows a systematic three-stage approach:

1. **Stochastic Data Generation** → Produce random samples using simulation parameters
2. **Model Training & Evaluation** → Apply multiple ML algorithms to simulated data
3. **Comparative Visualization** → Generate graphical representations of performance metrics

## Technical Configuration

**Simulation Engine:** SimPy (Discrete-Event Simulation Library)  
**Data Generation Method:** Synthetic dataset produced through programmatic simulation  
**Iteration Count:** 1,000 simulation runs for statistical validity  

**Machine Learning Models Evaluated:**
- Linear Regression
- Decision Tree Classifier
- Random Forest Ensemble
- Support Vector Machine (SVM)
- K-Nearest Neighbors (KNN)

**Deliverable Format:** Structured tabular outputs with comparative metrics

## Research Objectives

This study aims to accomplish three primary goals:

1. **Simulation-Driven Data Creation:** Demonstrate the viability of using simulation frameworks as an alternative to traditional data collection methods, enabling controlled experimental conditions.

2. **Multi-Model Benchmarking:** Conduct a systematic comparison of diverse machine learning algorithms on identical synthetic data to identify optimal approaches for specific data characteristics.

3. **Visual Analytics:** Present data patterns and model performance through comprehensive graphical representations, facilitating intuitive understanding of algorithmic behavior.

## Experimental Results

### Generated Synthetic Dataset:
The simulation produced a comprehensive dataset with multiple features and target variables, enabling robust model training and testing scenarios.

<img width="1489" height="738" alt="image" src="https://github.com/user-attachments/assets/ffe6b418-f749-426f-aac5-f191aa9aef98" />

---

### Comparative Model Performance Analysis:
Performance metrics across all evaluated algorithms reveal distinct strengths and weaknesses, providing insights into model selection for simulation-based datasets.

<img width="1238" height="485" alt="image" src="https://github.com/user-attachments/assets/169891da-a53f-4649-8d29-30813a435506" />

## Key Insights

The simulation-based approach offers several advantages including reproducibility, scalability, and the ability to generate edge cases that may be rare in real-world data collection scenarios.
