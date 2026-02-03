from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="Topsis-Saumil-102303862",  
    version="1.0.2",
    author="Saumil Makkar",
    author_email="saumilmakkar@example.com",  
    description="A Python package for TOPSIS (Technique for Order of Preference by Similarity to Ideal Solution) multi-criteria decision analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SaumilMakkar/UCS654",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Mathematics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "pandas>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "topsis=topsis.topsis:main",
        ],
    },
    keywords="topsis, mcdm, decision-making, multi-criteria, optimization",
    project_urls={
        "Bug Reports": "https://github.com/SaumilMakkar/UCS654/issues",
        "Source": "https://github.com/SaumilMakkar/UCS654",
    },
)
