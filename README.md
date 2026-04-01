# Math Problem Solver

A Python desktop application that solves math problems with step-by-step explanations.

**Built by Dr. Shir Sivroni** — Mathematics Lecturer, PhD Computational Electrophysiology

## Screenshot

![Math Solver Screenshot](screenshot.png)

## Features
- **Equation solving:** `x**2 - 4 = 0` → x = [-2, 2] with verification
- **Derivatives:** `diff(x**3 + 2*x)` → 6x with steps
- **Integrals:** `integrate(x**2)` → x³/3 + C
- **Arithmetic:** `2 + 3 * 4` → 14
- **Expand/Factor:** `(x+1)**3` → x³ + 3x² + 3x + 1

## Requirements
- Python 3.x
- SymPy (`pip install sympy`)

## How to Run
```
pip install sympy
python math_solver.py
```

## How It Works
1. Enter a math problem in the input field
2. Click "Solve" or press Enter
3. See the step-by-step solution

Clean, well-commented Python code using Tkinter GUI and SymPy for symbolic mathematics.
