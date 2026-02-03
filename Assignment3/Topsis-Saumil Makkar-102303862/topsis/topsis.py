"""
============================================================
TOPSIS – Technique for Order of Preference by
         Similarity to Ideal Solution
============================================================
Usage:
  python topsis.py <InputDataFile> <Weights> <Impacts> <OutputResultFileName>

Example:
  python topsis.py data.csv "1,1,1,2" "+,+,-,+" output-result.csv
============================================================
"""

import sys
import os
import csv
import math


# ──────────────────────────────────────────────────────────
#  VALIDATION HELPERS
# ──────────────────────────────────────────────────────────

def check_argument_count():
    """Exactly 4 arguments must follow the script name."""
    if len(sys.argv) != 5:
        print("Error: Incorrect number of parameters.")
        print("Usage : topsis <InputFile> <Weights> <Impacts> <OutputFile>")
        print("Example: topsis data.csv \"1,1,1,2\" \"+,+,-,+\" result.csv")
        sys.exit(1)


def check_file_exists(path):
    if not os.path.isfile(path):
        print(f"Error: Input file '{path}' not found.")
        sys.exit(1)


def read_input(path):
    """Return header (list) and rows (list-of-lists of strings)."""
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = [row for row in reader if any(cell.strip() for cell in row)]
    if len(rows) < 2:
        print("Error: Input file must have a header and at least one data row.")
        sys.exit(1)
    return rows[0], rows[1:]


def check_min_columns(header):
    if len(header) < 3:
        print("Error: Input file must contain three or more columns "
              "(1 name column + at least 2 numeric criteria columns).")
        sys.exit(1)


def check_numeric(data_rows):
    """Columns index 1 … end must be numeric in every row."""
    for r_idx, row in enumerate(data_rows, start=2):
        for c_idx in range(1, len(row)):
            try:
                float(row[c_idx])
            except ValueError:
                print(f"Error: Non-numeric value '{row[c_idx].strip()}' "
                      f"in row {r_idx}, column {c_idx + 1}.")
                sys.exit(1)


def parse_weights(weight_str, n_criteria):
    parts = [w.strip() for w in weight_str.split(",")]
    if len(parts) != n_criteria:
        print(f"Error: Number of weights ({len(parts)}) does not match "
              f"number of criteria columns ({n_criteria}). "
              f"Weights must be comma-separated.")
        sys.exit(1)
    weights = []
    for p in parts:
        try:
            weights.append(float(p))
        except ValueError:
            print(f"Error: '{p}' is not a valid weight. Weights must be numeric and comma-separated.")
            sys.exit(1)
    return weights


def parse_impacts(impact_str, n_criteria):
    parts = [i.strip() for i in impact_str.split(",")]
    if len(parts) != n_criteria:
        print(f"Error: Number of impacts ({len(parts)}) does not match "
              f"number of criteria columns ({n_criteria}). "
              f"Impacts must be comma-separated.")
        sys.exit(1)
    for p in parts:
        if p not in ("+", "-"):
            print(f"Error: Invalid impact value '{p}'. "
                  f"Each impact must be '+' (positive) or '-' (negative), comma-separated.")
            sys.exit(1)
    return parts


# ──────────────────────────────────────────────────────────
#  TOPSIS COMPUTATION
# ──────────────────────────────────────────────────────────

def topsis(matrix, weights, impacts):
    """
    Perform TOPSIS analysis on the given decision matrix.
    
    Parameters
    ----------
    matrix  : list[list[float]]   shape (n_alternatives, n_criteria)
              Decision matrix with alternatives as rows and criteria as columns
    weights : list[float]         length n_criteria
              Weights for each criterion
    impacts : list[str]           '+' or '-', length n_criteria
              Impact direction: '+' for benefit criteria, '-' for cost criteria

    Returns
    -------
    scores  : list[float]   TOPSIS score (0-100) per alternative
    ranks   : list[int]     rank (1 = best)
    
    Example
    -------
    >>> matrix = [[250, 16, 12], [200, 16, 8], [300, 32, 16]]
    >>> weights = [0.25, 0.25, 0.50]
    >>> impacts = ['+', '+', '-']
    >>> scores, ranks = topsis(matrix, weights, impacts)
    """
    rows = len(matrix)
    cols = len(matrix[0])

    # ── 1. Vector Normalisation  R_ij = X_ij / sqrt(sum X_ij^2) ──
    norm = [[0.0] * cols for _ in range(rows)]
    for j in range(cols):
        denom = math.sqrt(sum(matrix[i][j] ** 2 for i in range(rows)))
        for i in range(rows):
            norm[i][j] = matrix[i][j] / denom if denom != 0 else 0.0

    # ── 2. Weighted Normalisation  V_ij = W_j * R_ij ──
    v = [[norm[i][j] * weights[j] for j in range(cols)] for i in range(rows)]

    # ── 3. Ideal Best (A+) and Ideal Worst (A-) ──
    a_pos = [0.0] * cols
    a_neg = [0.0] * cols
    for j in range(cols):
        col = [v[i][j] for i in range(rows)]
        if impacts[j] == "+":
            a_pos[j], a_neg[j] = max(col), min(col)
        else:                                   # negative / cost criterion
            a_pos[j], a_neg[j] = min(col), max(col)

    # ── 4. Euclidean Distances to A+ and A- ──
    s_pos = [math.sqrt(sum((v[i][j] - a_pos[j]) ** 2 for j in range(cols))) for i in range(rows)]
    s_neg = [math.sqrt(sum((v[i][j] - a_neg[j]) ** 2 for j in range(cols))) for i in range(rows)]

    # ── 5. TOPSIS Score  C_i = S- / (S+ + S-) * 100 ──
    scores = []
    for i in range(rows):
        total = s_pos[i] + s_neg[i]
        scores.append(round((s_neg[i] / total) * 100, 2) if total != 0 else 0.0)

    # ── 6. Rank  (highest score => rank 1) ──
    sorted_idx = sorted(range(rows), key=lambda i: scores[i], reverse=True)
    ranks = [0] * rows
    for rank_val, idx in enumerate(sorted_idx, start=1):
        ranks[idx] = rank_val

    return scores, ranks


# ──────────────────────────────────────────────────────────
#  OUTPUT
# ──────────────────────────────────────────────────────────

def write_output(header, names, matrix, scores, ranks, out_path):
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(list(header) + ["Topsis Score", "Rank"])
        for i in range(len(names)):
            row = [names[i]] + matrix[i] + [scores[i], ranks[i]]
            writer.writerow(row)


# ──────────────────────────────────────────────────────────
#  MAIN
# ──────────────────────────────────────────────────────────

def main():
    """
    Main entry point for command-line usage.
    """
    # 1. argument count
    check_argument_count()

    input_file  = sys.argv[1]
    weight_str  = sys.argv[2]
    impact_str  = sys.argv[3]
    output_file = sys.argv[4]

    # 2. file exists
    check_file_exists(input_file)

    # 3. read CSV
    header, data_rows = read_input(input_file)

    # 4. >= 3 columns
    check_min_columns(header)

    # 5. numeric check on criteria columns
    check_numeric(data_rows)

    # 6. derive counts
    n_criteria = len(header) - 1

    # 7. weights & impacts (count + format validation inside)
    weights = parse_weights(weight_str, n_criteria)
    impacts = parse_impacts(impact_str, n_criteria)

    # 8. build numeric matrix & name list
    names  = [row[0].strip() for row in data_rows]
    matrix = [[float(row[c]) for c in range(1, len(row))] for row in data_rows]

    # 9. run TOPSIS
    scores, ranks = topsis(matrix, weights, impacts)

    # 10. save
    write_output(header, names, matrix, scores, ranks, output_file)
    print(f"TOPSIS completed. Results saved to '{output_file}'.")


if __name__ == "__main__":
    main()
