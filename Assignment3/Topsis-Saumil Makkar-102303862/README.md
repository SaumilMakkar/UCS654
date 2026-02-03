# Topsis-Saumil-102303862

A Python package implementing **TOPSIS** (Technique for Order of Preference by Similarity to Ideal Solution) for multi-criteria decision analysis (MCDM).

## What is TOPSIS?

TOPSIS is a multi-criteria decision-making method that helps rank alternatives based on multiple criteria. It works by:
1. Calculating the distance of each alternative from the ideal best and ideal worst solutions
2. Ranking alternatives based on their relative closeness to the ideal solution

## Installation

```bash
pip install Topsis-Saumil-102303862
```

## Usage

### Command Line Interface

After installation, you can use TOPSIS directly from the command line:

```bash
topsis <InputDataFile> <Weights> <Impacts> <OutputResultFileName>
```

### Parameters

- **InputDataFile**: CSV file with the first column as object/alternative names and remaining columns as criteria
- **Weights**: Comma-separated weights for each criterion (e.g., "1,1,2,1")
- **Impacts**: Comma-separated impacts for each criterion, either '+' (benefit) or '-' (cost) (e.g., "+,+,-,+")
- **OutputResultFileName**: Name of the output CSV file with TOPSIS scores and ranks

### Example

#### Input File (data.csv)

```csv
Fund Name,P1,P2,P3,P4,P5
M1,0.67,0.45,6.5,42.6,12.56
M2,0.60,0.36,3.6,53.3,14.47
M3,0.82,0.67,3.8,63.1,17.10
M4,0.60,0.36,3.5,69.2,18.42
M5,0.76,0.58,4.8,43.0,12.29
M6,0.69,0.48,6.6,48.7,14.12
M7,0.79,0.62,4.8,59.2,16.35
M8,0.84,0.71,6.5,34.5,10.64
```

#### Command

```bash
topsis data.csv "1,1,1,1,1" "+,+,-,+,+" result.csv
```

#### Output File (result.csv)

The output will include the original data plus two additional columns:
- **Topsis Score**: A score between 0-100 indicating closeness to the ideal solution
- **Rank**: Ranking based on TOPSIS score (1 = best)

```csv
Fund Name,P1,P2,P3,P4,P5,Topsis Score,Rank
M1,0.67,0.45,6.5,42.6,12.56,21.52,8
M2,0.60,0.36,3.6,53.3,14.47,46.80,4
M3,0.82,0.67,3.8,63.1,17.10,86.15,1
M4,0.60,0.36,3.5,69.2,18.42,58.85,3
M5,0.76,0.58,4.8,43.0,12.29,45.08,5
M6,0.69,0.48,6.6,48.7,14.12,32.66,7
M7,0.79,0.62,4.8,59.2,16.35,69.55,2
M8,0.84,0.71,6.5,34.5,10.64,41.42,6
```

### Using in Python Code

You can also use the TOPSIS package programmatically:

```python
from topsis.topsis import topsis
import pandas as pd

# Your data as a list of lists (excluding the first column with names)
matrix = [
    [0.67, 0.45, 6.5, 42.6, 12.56],
    [0.60, 0.36, 3.6, 53.3, 14.47],
    [0.82, 0.67, 3.8, 63.1, 17.10],
]

weights = [1, 1, 1, 1, 1]
impacts = ["+", "+", "-", "+", "+"]

scores, ranks = topsis(matrix, weights, impacts)
print("Scores:", scores)
print("Ranks:", ranks)
```

## Input Validation

The package performs comprehensive input validation:

✅ Checks for correct number of command-line parameters  
✅ Validates file existence  
✅ Ensures minimum 3 columns (1 name + 2 criteria)  
✅ Verifies all criteria values are numeric  
✅ Confirms weights and impacts count matches criteria count  
✅ Validates impacts are only '+' or '-'  
✅ Ensures comma-separated format for weights and impacts  

## Error Messages

The package provides clear, actionable error messages:

```bash
# Wrong number of parameters
Error: Incorrect number of parameters.
Usage : topsis <InputFile> <Weights> <Impacts> <OutputFile>

# File not found
Error: Input file 'data.csv' not found.

# Non-numeric value
Error: Non-numeric value 'abc' in row 2, column 3.

# Mismatched weights
Error: Number of weights (3) does not match criteria columns (5).

# Invalid impact
Error: Invalid impact '0'. Must be '+' or '-'.
```

## Algorithm Steps

1. **Normalization**: Convert the decision matrix using vector normalization
2. **Weighted Normalization**: Multiply normalized values by their weights
3. **Ideal Solutions**: Determine ideal best (A+) and ideal worst (A-) solutions
4. **Distance Calculation**: Calculate Euclidean distances from ideal solutions
5. **TOPSIS Score**: Calculate relative closeness to ideal solution
6. **Ranking**: Rank alternatives based on TOPSIS scores

## Requirements

- Python >= 3.7
- pandas >= 1.0.0

## License

MIT License

## Author

**Saumil Makkar**  
Email: saumilmakkar@example.com  
GitHub: https://github.com/SaumilMakkar/UCS654

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Issues

If you encounter any problems, please file an issue at:
https://github.com/SaumilMakkar/UCS654/issues

## Changelog

### Version 1.0.0 (2024)
- Initial release
- Command-line interface
- Comprehensive input validation
- Clear error messages
- Support for any number of criteria
- Handles both benefit (+) and cost (-) criteria

## References

- Hwang, C.L.; Yoon, K. (1981). Multiple Attribute Decision Making: Methods and Applications. New York: Springer-Verlag.
- Yoon, K. (1987). "A reconciliation among discrete compromise situations". Journal of the Operational Research Society. 38 (3): 277–286.
- Original Implementation: https://github.com/SaumilMakkar/UCS654/blob/main/Assignment3/Assignment3UCS654.ipynb

## Keywords

TOPSIS, MCDM, Multi-Criteria Decision Making, Decision Analysis, Optimization, Ranking, Python
