from ase.io import read, write
from pathlib import Path

PROJECT_ROOT=Path(__file__).parents[0]

file1 = f"{PROJECT_ROOT}/lammps.extxyz"
file2 = f"{PROJECT_ROOT}/train.extxyz"

frames1 = read(file1, ":")
frames2 = read(file2, ":")

combined = frames1 + frames2

write(f"{PROJECT_ROOT}/combined.extyxz", combined, format="extxyz")