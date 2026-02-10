# TOPSIS-Based Evaluation of Pre-Trained Models for Text Classification

## Project Overview
This project implements the TOPSIS (Technique for Order of Preference by Similarity to Ideal Solution) method to systematically evaluate and rank various pre-trained models for text classification tasks.

## Workflow
1. **Data Acquisition** → Collect text dataset
2. **Model Evaluation** → Test multiple pre-trained models
3. **Metrics Computation** → Calculate performance indicators
4. **TOPSIS Analysis** → Determine optimal model ranking

## Implementation Details

**Dataset Source:** `stanfordnlp/sst2.csv`

**Configuration Parameters:**
- **Weights:** Positive real numbers (w > 0)
- **Impacts:** Binary indicators (+/-)

**Deliverables:** Comparative tables and visualization charts

## Project Goals
- Implement TOPSIS mathematical framework for model selection
- Identify the top-performing model for text classification
- Analyze sensitivity of rankings to weight and impact variations

## Experimental Results

### Input Configuration:
<img width="518" height="625" alt="image" src="https://github.com/user-attachments/assets/19497b27-281c-4d5d-89fd-6765b5605743" />

---

### TOPSIS Ranking Results:
<img width="1236" height="489" alt="image" src="https://github.com/user-attachments/assets/86510cf7-7440-41ec-a247-2b0ad23991b6" />

---

### Performance Visualizations:
<img width="789" height="585" alt="image" src="https://github.com/user-attachments/assets/3e3d614d-1e6b-4cab-acce-700d44718403" />

<img width="789" height="588" alt="image" src="https://github.com/user-attachments/assets/d5bb09b8-76d4-4506-855b-cf7086a8244a" />
