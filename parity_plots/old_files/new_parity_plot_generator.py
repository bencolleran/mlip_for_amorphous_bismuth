#!/usr/bin/env python3
# extract_and_plot.py
"""
Reads an extxyz file, builds in-memory pandas DataFrames for energies and forces,
and writes parity plots. Can be run from terminal, imported, run in a REPL, or
double-clicked — it will use a GUI file picker if available, otherwise prompt.
"""

import sys
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[0]

num_re = re.compile(
    r'REF_energy\s*=\s*([-\d.eE+]+)|\benergy\s*=\s*([-\d.eE+]+)'
)

def read_extxyz_to_dfs(path):
    energy_rows = []
    force_rows = []
    with open(path, 'r') as f:
        frame = 0
        while True:
            nat = f.readline()
            if not nat:
                break
            n = int(nat.split()[0])
            header = f.readline() or ""

            ref = en = None
            for m in re.finditer(num_re, header):
                if m.group(1):
                    ref = float(m.group(1))
                if m.group(2):
                    en = float(m.group(2))

            en_pa  = en  / n if en  is not None else np.nan
            ref_pa = ref / n if ref is not None else np.nan

            energy_rows.append((frame, en_pa, ref_pa))

            for i in range(n):
                line = f.readline()
                if not line:
                    raise EOFError("Unexpected EOF while reading atoms")
                toks = line.split()
                if len(toks) < 10:
                    raise ValueError(f"Unexpected atom line format (len={len(toks)}): {line!r}")

                REF_fx = float(toks[4]); REF_fy = float(toks[5]); REF_fz = float(toks[6])
                fx = float(toks[7]); fy = float(toks[8]); fz = float(toks[9])

                force_rows.append((frame, i, REF_fx, REF_fy, REF_fz, fx, fy, fz,))

            frame += 1

    df_e = pd.DataFrame(energy_rows, columns=("frame","energy","REF_energy"))
    df_f = pd.DataFrame(force_rows, columns=("frame","atom","fx","fy","fz","REF_fx","REF_fy","REF_fz"))
    return df_e, df_f

def parity_plot_energy(df, name="energies",path=f"{PROJECT_ROOT}/potential_data"):
    x = df["energy"].to_numpy()
    y = df["REF_energy"].to_numpy()
    mask = ~np.isnan(x) & ~np.isnan(y)
    x = x[mask]; y = y[mask]
    if x.size == 0:
        print("No paired energy data to plot.")
        return
    rmse = np.sqrt(np.mean((x - y)**2))*1000
    print(f"{name} RMSE = {rmse}")
    plt.figure(figsize=(6,4), dpi=150)
    plt.scatter(x, y, marker='x', s=10)
    lims = [min(x.min(), y.min()), max(x.max(), y.max())]
    plt.plot(lims, lims)
    plt.xlabel("predicted energy per atom / eV")
    plt.ylabel("DFT energy per atom / eV")
    plt.title(f"{name} RMSE={rmse:.6f} meV")
    plt.savefig(f"{path}/{name}_plot.png", dpi=600, bbox_inches="tight")
    plt.close()

def parity_plot_forces(df, name="forces",path=f"{PROJECT_ROOT}/potential_data"):
    x = df[['fx','fy','fz']].to_numpy().ravel()
    y = df[['REF_fx','REF_fy','REF_fz']].to_numpy().ravel()
    if x.size == 0:
        print("No force data to plot.")
        return
    rmse = np.sqrt(np.mean((x - y)**2))*1000
    print(f"{name} RMSE = {rmse}")
    plt.figure(figsize=(6,4), dpi=150)
    plt.scatter(x, y, marker='x', s=10)
    lims = [min(x.min(), y.min()), max(x.max(), y.max())]
    plt.plot(lims, lims)
    plt.xlabel("predicted force component / eV/A")
    plt.ylabel("DFT force component / eV/A")
    plt.title(f"{name} RMSE={rmse:.6f} meV/A")
    plt.savefig(f"{path}/{name}_plot.png", dpi=600, bbox_inches="tight")
    plt.close()

if __name__ == "__main__":
    var=2
    if var==1:
        path=f"{PROJECT_ROOT}/potential_data/correct_extended_data_mlip"
        data_path=path + "/quip_new_test.extxyz"
        df_e, df_f = read_extxyz_to_dfs(data_path)
        parity_plot_energy(df_e, name="newest_energies",path=path)
        parity_plot_forces(df_f, name="newest_forces",path=path)
    elif var==2:
        path=f"{PROJECT_ROOT}/potential_data/initial_autoplex_mlip"
        data_path=path + "/quip_test.extxyz"
        df_e, df_f = read_extxyz_to_dfs(data_path)
        parity_plot_energy(df_e, name="energies",path=path)
        parity_plot_forces(df_f, name="forces",path=path)
    else:
        path=f"{PROJECT_ROOT}/potential_data/correct_extended_data_mlip"
        data_path=path + "/new_potential_on_old_test_quip_test.extxyz"
        df_e, df_f = read_extxyz_to_dfs(data_path)
        parity_plot_energy(df_e, name="new_on_old_energies",path=path)
        parity_plot_forces(df_f, name="new_on_old_forces",path=path)