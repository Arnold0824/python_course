import numpy as np
import pandas as pd

print("NumPy version:", np.__version__)
print("pandas version:", pd.__version__)

from pathlib import Path

DATA_DIR = Path("public\courses\python\ch08")
scores_path = DATA_DIR / "scores.csv"

scores_df = pd.read_csv(scores_path)
print(scores_df.head())
python_scores = np.array([92, 95, 80, 70, 98, 66])

print(python_scores)
print("维度:", python_scores.ndim)
print("形状:", python_scores.shape)
print("类型:", python_scores.dtype)

print(np.arange(1, 10, 2))
print(np.linspace(0, 1, 5))
print(np.zeros((2, 3)))
print(np.ones((2, 3)))

rng = np.random.default_rng(42)
print(rng.integers(60, 101, size=(3, 4)))

raw_scores = np.array([58, 69, 80, 92, 100])
bonus_scores = raw_scores + 5
bonus_scores = np.minimum(bonus_scores, 100)

print("原始成绩:", raw_scores)
print("加分后:", bonus_scores)
print("是否及格:", bonus_scores >= 60)