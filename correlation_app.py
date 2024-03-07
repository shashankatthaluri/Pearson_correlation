import tkinter as tk
from tkinter import messagebox, filedialog
import matplotlib.pyplot as plt
import numpy as np

class CorrelationApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Correlation Coefficient App")

        self.x_values = []
        self.y_values = []

        self.create_widgets()

    def create_widgets(self):
        # Input fields
        tk.Label(self.master, text="X Coordinate:").grid(row=0, column=0)
        tk.Label(self.master, text="Y Coordinate:").grid(row=1, column=0)

        self.x_entry = tk.Entry(self.master)
        self.y_entry = tk.Entry(self.master)

        self.x_entry.grid(row=0, column=1)
        self.y_entry.grid(row=1, column=1)

        # Buttons
        tk.Button(self.master, text="Add", command=self.add_data).grid(row=2, column=0, columnspan=2, pady=10)
        tk.Button(self.master, text="Calculate", command=self.calculate).grid(row=3, column=0, columnspan=2, pady=10)
        tk.Button(self.master, text="Load Data", command=self.load_data).grid(row=4, column=0, columnspan=2, pady=10)

        # Result area
        self.result_text = tk.Text(self.master, height=10, width=40)
        self.result_text.grid(row=5, column=0, columnspan=2)

    def add_data(self):
        x_value = self.x_entry.get()
        y_value = self.y_entry.get()

        try:
            x_value = float(x_value)
            y_value = float(y_value)

            self.x_values.append(x_value)
            self.y_values.append(y_value)

            self.result_text.insert(tk.END, f"Added: ({x_value}, {y_value})\n")

            # Clear entries
            self.x_entry.delete(0, tk.END)
            self.y_entry.delete(0, tk.END)

        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter valid numbers.")

    def calculate(self):
        if not self.x_values or not self.y_values:
            messagebox.showerror("Error", "Please add data points before calculating.")
            return

        x_mean = np.mean(self.x_values)
        y_mean = np.mean(self.y_values)
        x_std = np.std(self.x_values)
        y_std = np.std(self.y_values)

        covariance = np.cov(self.x_values, self.y_values)[0, 1]
        correlation_coefficient = covariance / (x_std * y_std)

        result = f"Arithmetic Mean (X): {x_mean:.2f}\n" \
                 f"Arithmetic Mean (Y): {y_mean:.2f}\n" \
                 f"Standard Deviation (X): {x_std:.2f}\n" \
                 f"Standard Deviation (Y): {y_std:.2f}\n" \
                 f"Pearson Correlation Coefficient: {correlation_coefficient:.2f}\n"

        self.result_text.delete(1.0, tk.END)  # Clear previous results
        self.result_text.insert(tk.END, result)

        # Bonus: Scatter plot
        plt.scatter(self.x_values, self.y_values)
        plt.title("Scatter Plot")
        plt.xlabel("X Coordinate")
        plt.ylabel("Y Coordinate")
        plt.show()

    def load_data(self):
        file_path = filedialog.askopenfilename(title="Select Data File", filetypes=[("Text files", "*.txt")])

        if not file_path:
            return

        try:
            data = np.loadtxt(file_path, delimiter=',')
            self.x_values.extend(data[:, 0])
            self.y_values.extend(data[:, 1])

            self.result_text.insert(tk.END, f"Loaded data from file: {file_path}\n")
        except Exception as e:
            messagebox.showerror("Error", f"Error loading data from file: {e}")

# Main
if __name__ == "__main__":
    root = tk.Tk()
    app = CorrelationApp(root)
    root.mainloop()
