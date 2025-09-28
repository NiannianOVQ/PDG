====================================================================
README for Supplementary Code
====================================================================

This folder contains the source code used in the paper:
"The cooperation evolution in a three-strategy model including enforcers with the ability to reward, punish and assess"
Submitted to Chaos, Solitons & Fractals (Elsevier).

The code is provided in two parts:
1. Python scripts for running the evolutionary game simulation and computing results.
2. MATLAB scripts for generating figures based on the Python results.

--------------------------------------------------------------------
1. Requirements
--------------------------------------------------------------------
- Python 3.9
  Required packages:
    * numpy
    * numba
    * scipy

- MATLAB R2022a

--------------------------------------------------------------------
2. Usage
--------------------------------------------------------------------
Python (Simulation):
  1. Open main_analysis.py in PyCharm or any Python IDE.
  2. Make sure the working directory is set to this folder (Supplementary_Code).
  3. Run the script.
  4. The output arrays f0, f1, f2 will be saved as MATLAB-compatible file: ./fractions.txt
	These arrays contain the evolution of D/C/E fractions over time, ready for plotting in MATLAB.

MATLAB (Figures):
  1. Open plot_figures.m in MATLAB.
  2. Make sure fractions.mat is in the same folder.
  3. Run the script: plot_figures
  4. The generated figures will be saved in the current folder.

====================================================================
End of README
====================================================================
