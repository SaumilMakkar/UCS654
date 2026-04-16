### Sampling Assignment – Credit Card Fraud Detection

This assignment compares **different sampling techniques** for handling class imbalance on the well‑known **credit card fraud detection dataset** and evaluates several **classification models** on the sampled data.

### Dataset

- **File**: `Creditcard_data.csv`  
- **Rows/Columns**: 284,807 transactions, 31 columns (`Time`, `V1`–`V28`, `Amount`, `Class`)  
- **Target**: `Class` (0 = non‑fraud, 1 = fraud)  

Dataset preview (first few rows):

![Dataset preview](Files/Dataset.png)

### Sampling Methods Implemented

From the full DataFrame `df`, the notebook constructs five different samples:

- **Simple Random Sampling**: `df.sample(frac=0.5, random_state=42)`  
- **Systematic Sampling**: `df.iloc[::2]` (every 2nd record)  
- **Stratified Sampling**: `train_test_split(..., train_size=0.5, stratify=df["Class"])`  
- **Cluster Sampling**:  
  - PCA reduces features to 2D (`PCA(n_components=2)`)  
  - `KMeans(n_clusters=5)` creates clusters  
  - Keep clusters 0 and 1, then drop the helper `Cluster` column  
- **Bootstrap Sampling**: `df.sample(frac=1, replace=True, random_state=42)`  

These are stored in a dictionary:

- `{"Simple Random": simple_random, "Systematic": systematic, "Stratified": stratified, "Cluster": cluster, "Bootstrap": bootstrap}`

### Models Evaluated

Each sampling method is combined with the following models:

- **Logistic Regression** (`LogisticRegression(max_iter=1000)`)  
- **Decision Tree** (`DecisionTreeClassifier()`)  
- **Random Forest** (`RandomForestClassifier(n_estimators=100)`)  
- **SVM** (`SVC()`)  
- **Naive Bayes** (`GaussianNB()`)  

Workflow per sampling method:

- Split into train/test (stratified on `Class`).  
- Standardize features with `StandardScaler`.  
- Train each model on the sampled training set.  
- Evaluate on the **same global test set** (`X_test`, `y_test`) derived from the original data.  
- Store **accuracy** for each (sampling method, model) pair.

### Results Table

The notebook aggregates all accuracies into a `results_df` DataFrame and then pivots it to `final_table`:

- **Index**: `Model`  
- **Columns**: `Sampling Method`  
- **Values**: `Accuracy` (rounded to 4 decimals)  

`matplotlib` is used to render this pivot as a nicely formatted table figure.

Example output table:

![Output table](Files/output.png)

### How to Run

- **Prerequisites**: Python, Jupyter (or VS Code with Jupyter), and the following packages:  
  - `pandas`, `numpy`, `scikit-learn`, `matplotlib`  

1. Open `assignment.ipynb` inside the `Sampling Assignment` folder.  
2. Ensure the notebook kernel uses the correct environment (where the packages above are installed).  
3. Run all cells in order:
   - Imports and data loading.  
   - Train/test split and scaling.  
   - Sampling method construction.  
   - Model training loop and accuracy computation.  
   - Final table creation and table plot.  

### What to Look At / Interpretation

- **Compare rows** (models) across **columns** (sampling methods) to see how sampling affects accuracy.  
- Notice how methods like **Stratified** and **Bootstrap** typically maintain performance on the minority (fraud) class better than naive simple or systematic sampling.  
- Use the table to discuss which combination of **sampling strategy + model** is most robust for imbalanced fraud detection.

