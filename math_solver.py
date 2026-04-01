"""
Math Problem Solver — Desktop Application
Built by Dr. Shir Sivroni
Solves algebra, arithmetic, calculus problems with step-by-step explanations.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import sympy as sp
from sympy import symbols, solve, diff, integrate, simplify, factor, expand
from sympy import sin, cos, tan, log, exp, sqrt, pi, oo
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

# Setup
x, y, z, t = symbols('x y z t')

TRANSFORMATIONS = standard_transformations + (implicit_multiplication_application,)


def solve_problem(expression_str):
    """Parse and solve a math problem, returning step-by-step solution."""
    steps = []
    expr_str = expression_str.strip()

    if not expr_str:
        return "Please enter a math problem."

    steps.append(f"Input: {expr_str}")
    steps.append("-" * 40)

    try:
        # CASE 1: Equation solving (contains '=')
        if '=' in expr_str and '==' not in expr_str:
            parts = expr_str.split('=')
            left = parse_expr(parts[0].strip(), transformations=TRANSFORMATIONS)
            right = parse_expr(parts[1].strip(), transformations=TRANSFORMATIONS)
            equation = left - right

            steps.append(f"Step 1: Rearrange to standard form")
            steps.append(f"   {left} = {right}")
            steps.append(f"   {equation} = 0")
            steps.append("")

            solutions = solve(equation, x)
            steps.append(f"Step 2: Solve for x")
            if solutions:
                for i, sol in enumerate(solutions):
                    steps.append(f"   x_{i+1} = {sol}")
                    # Verify
                    check = equation.subs(x, sol)
                    steps.append(f"   Verification: substituting x = {sol} gives {simplify(check)} [OK]")
            else:
                steps.append("   No solution found.")

            steps.append("")
            steps.append(f"Final Answer: x = {solutions}")
            return "\n".join(steps)

        # Parse the expression
        expr = parse_expr(expr_str, transformations=TRANSFORMATIONS)

        # CASE 2: Derivative (starts with 'diff' or 'd/dx')
        if expr_str.lower().startswith(('diff(', 'derivative', "d/dx")):
            if expr_str.lower().startswith("d/dx"):
                inner = expr_str[4:].strip().strip("()")
                expr = parse_expr(inner, transformations=TRANSFORMATIONS)
            else:
                expr = parse_expr(expr_str, transformations=TRANSFORMATIONS)

            result = diff(expr, x)
            steps.append(f"Step 1: Find the derivative of {expr} with respect to x")
            steps.append(f"Step 2: Apply differentiation rules")
            steps.append(f"   d/dx [{expr}]")
            steps.append(f"   = {result}")
            steps.append("")
            simplified = simplify(result)
            if simplified != result:
                steps.append(f"Step 3: Simplify")
                steps.append(f"   = {simplified}")
            steps.append("")
            steps.append(f"Final Answer: {simplified}")
            return "\n".join(steps)

        # CASE 3: Integration (starts with 'int' or 'integrate')
        if expr_str.lower().startswith(('int(', 'integrate', 'integral')):
            inner = expr_str.split("(", 1)[1].rsplit(")", 1)[0] if "(" in expr_str else expr_str[3:]
            expr = parse_expr(inner.strip(), transformations=TRANSFORMATIONS)

            result = integrate(expr, x)
            steps.append(f"Step 1: Find the integral of {expr} with respect to x")
            steps.append(f"Step 2: Apply integration rules")
            steps.append(f"   Integral {expr} dx")
            steps.append(f"   = {result} + C")
            steps.append("")
            steps.append(f"Final Answer: {result} + C")
            return "\n".join(steps)

        # CASE 4: Simplification / Evaluation
        simplified = simplify(expr)
        factored = factor(expr)
        expanded = expand(expr)

        steps.append(f"Step 1: Parse expression")
        steps.append(f"   {expr}")
        steps.append("")

        if expanded != expr:
            steps.append(f"Step 2: Expand")
            steps.append(f"   = {expanded}")
            steps.append("")

        if factored != expr and factored != expanded:
            steps.append(f"Step 3: Factor")
            steps.append(f"   = {factored}")
            steps.append("")

        if simplified != expr:
            steps.append(f"Step 4: Simplify")
            steps.append(f"   = {simplified}")
            steps.append("")

        # Check if it's purely numeric
        try:
            numerical = float(expr.evalf())
            steps.append(f"Numerical value: {numerical}")
        except:
            pass

        steps.append(f"Final Answer: {simplified}")
        return "\n".join(steps)

    except Exception as e:
        steps.append(f"Error: Could not parse '{expr_str}'")
        steps.append(f"Details: {str(e)}")
        steps.append("")
        steps.append("Supported formats:")
        steps.append("  Arithmetic:    2 + 3 * 4")
        steps.append("  Algebra:       x**2 + 3*x - 4 = 0")
        steps.append("  Derivative:    diff(x**3 + 2*x)")
        steps.append("  Integral:      integrate(x**2 + 1)")
        steps.append("  Simplify:      (x**2 - 1)/(x - 1)")
        return "\n".join(steps)


# ============================================================
# GUI
# ============================================================

class MathSolverApp:
    def __init__(self, root):
        root.title("Math Problem Solver — Dr. Shir Sivroni")
        root.geometry("700x600")
        root.configure(bg="#0b1220")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Title.TLabel", font=("Segoe UI", 18), foreground="#11a8a0", background="#0b1220")
        style.configure("Sub.TLabel", font=("Segoe UI", 10), foreground="#94a3b8", background="#0b1220")
        style.configure("TButton", font=("Segoe UI", 12), padding=8)
        style.configure("TFrame", background="#0b1220")

        # Title
        title_frame = ttk.Frame(root, style="TFrame")
        title_frame.pack(pady=(20, 5))
        ttk.Label(title_frame, text="Math Problem Solver", style="Title.TLabel").pack()
        ttk.Label(title_frame, text="Enter a math problem and get a step-by-step solution", style="Sub.TLabel").pack()

        # Input frame
        input_frame = ttk.Frame(root, style="TFrame")
        input_frame.pack(pady=15, padx=30, fill="x")

        ttk.Label(input_frame, text="Enter your problem:", style="Sub.TLabel").pack(anchor="w")

        self.entry = tk.Entry(input_frame, font=("Consolas", 14), bg="#141d2b", fg="#e5e7eb",
                             insertbackground="#11a8a0", relief="flat", bd=8)
        self.entry.pack(fill="x", pady=(5, 10))
        self.entry.bind("<Return>", lambda e: self.solve())
        self.entry.focus()

        # Buttons
        btn_frame = ttk.Frame(root, style="TFrame")
        btn_frame.pack(pady=5)

        solve_btn = tk.Button(btn_frame, text="Solve", font=("Segoe UI", 12, "bold"),
                             bg="#11a8a0", fg="white", relief="flat", padx=20, pady=5,
                             command=self.solve, cursor="hand2")
        solve_btn.pack(side="left", padx=5)

        clear_btn = tk.Button(btn_frame, text="Clear", font=("Segoe UI", 12),
                             bg="#2d3a4f", fg="#94a3b8", relief="flat", padx=20, pady=5,
                             command=self.clear, cursor="hand2")
        clear_btn.pack(side="left", padx=5)

        # Examples
        examples_frame = ttk.Frame(root, style="TFrame")
        examples_frame.pack(pady=5)
        ttk.Label(examples_frame, text="Examples:", style="Sub.TLabel").pack(side="left", padx=5)

        examples = ["x**2 - 4 = 0", "diff(x**3 + 2*x)", "integrate(x**2)", "(x+1)**3"]
        for ex in examples:
            btn = tk.Button(examples_frame, text=ex, font=("Consolas", 9),
                          bg="#141d2b", fg="#a78bfa", relief="flat", padx=8, pady=2,
                          command=lambda e=ex: self.set_example(e), cursor="hand2")
            btn.pack(side="left", padx=3)

        # Output
        output_frame = ttk.Frame(root, style="TFrame")
        output_frame.pack(pady=10, padx=30, fill="both", expand=True)

        ttk.Label(output_frame, text="Solution:", style="Sub.TLabel").pack(anchor="w")

        self.output = scrolledtext.ScrolledText(output_frame, font=("Consolas", 12),
                                                bg="#141d2b", fg="#e5e7eb",
                                                insertbackground="#11a8a0", relief="flat",
                                                bd=8, wrap="word")
        self.output.pack(fill="both", expand=True, pady=(5, 0))

        # Footer
        footer = ttk.Label(root, text="© Dr. Shir Sivroni | Mathematics Lecturer | Technion BSc CS, TAU PhD",
                          style="Sub.TLabel")
        footer.pack(pady=(5, 10))

    def solve(self):
        problem = self.entry.get()
        result = solve_problem(problem)
        self.output.delete(1.0, tk.END)
        self.output.insert(tk.END, result)

    def clear(self):
        self.entry.delete(0, tk.END)
        self.output.delete(1.0, tk.END)

    def set_example(self, text):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, text)
        self.solve()


if __name__ == "__main__":
    root = tk.Tk()
    app = MathSolverApp(root)
    root.mainloop()
