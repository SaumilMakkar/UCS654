"""
Topsis-Saumil-102303862
======================

A Python package for TOPSIS (Technique for Order of Preference by 
Similarity to Ideal Solution) multi-criteria decision analysis.

Usage:
    Command Line:
        topsis <InputDataFile> <Weights> <Impacts> <OutputResultFileName>
    
    Python:
        from topsis.topsis import topsis
        scores, ranks = topsis(matrix, weights, impacts)

Author: Saumil Makkar
GitHub: https://github.com/SaumilMakkar/UCS654
License: MIT
"""

__version__ = "1.0.2"
__author__ = "Saumil Makkar"
__email__ = "saumilmakkar@example.com"

from topsis.topsis import topsis, main

__all__ = ["topsis", "main"]
