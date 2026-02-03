# TOPSIS Implementation

A Python implementation of TOPSIS (Technique for Order of Preference by Similarity to Ideal Solution) for multi-criteria decision analysis.

## What is TOPSIS?

TOPSIS is a multi-criteria decision-making method that ranks alternatives based on their geometric distance from the ideal solution. The best alternative is closest to the positive ideal solution and farthest from the negative ideal solution.

## Algorithm

1. **Normalization**: Convert decision matrix using vector normalization
2. **Weighted Matrix**: Multiply normalized values by criterion weights
3. **Ideal Solutions**: Identify positive ideal (best) and negative ideal (worst) solutions
4. **Distance Calculation**: Compute Euclidean distance from each alternative to both ideal solutions
5. **Relative Closeness**: Calculate TOPSIS score as ratio of distance to negative ideal over sum of both distances
6. **Ranking**: Rank alternatives by TOPSIS score in descending order

## Installation

```bash
pip install Topsis-Saumil-102203456
```

## Usage

### Command Line

```bash
topsis <InputDataFile> <Weights> <Impacts> <OutputResultFileName>
```

**Parameters:**
- InputDataFile: CSV file with alternatives in rows and criteria in columns (first column = names)
- Weights: Comma-separated numerical weights for each criterion
- Impacts: Comma-separated '+' (benefit) or '-' (cost) for each criterion
- OutputResultFileName: Path for output CSV with TOPSIS scores and ranks

**Example:**

```bash
topsis data.csv "1,1,1,2" "+,+,-,+" result.csv
```

### Input File Format

```csv
Fund Name,P1,P2,P3,P4
M1,0.84,0.71,6.5,42.6
M2,0.91,0.83,7.0,60.8
M3,0.79,0.62,4.8,46.2
```

### Output Format

Output includes original data plus two additional columns:
- **Topsis Score**: Relative closeness to ideal solution (0-100)
- **Rank**: Ranking based on score (1 = best)

### Python API

```python
from topsis.topsis import topsis

matrix = [[0.84, 0.71, 6.5, 42.6],
          [0.91, 0.83, 7.0, 60.8]]
weights = [1, 1, 1, 2]
impacts = ['+', '+', '-', '+']

scores, ranks = topsis(matrix, weights, impacts)
```

## Input Validation

The package validates:
- Correct number of parameters
- File existence
- Minimum 3 columns (1 name + 2 criteria)
- Numeric values in all criteria columns
- Matching counts for weights, impacts, and criteria
- Valid impact symbols ('+' or '-')
- Comma-separated format for weights and impacts

## Requirements

- Python 3.7 or higher
- pandas

## Error Handling

The package provides clear error messages for:
- Missing or incorrect parameters
- File not found
- Non-numeric values in data
- Mismatched dimensions (weights, impacts, criteria)
- Invalid impact symbols


## Author

Saumil Makkar


