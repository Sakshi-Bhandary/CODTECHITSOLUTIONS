import tkinter as tk


def on_click(button_text):
    current = entry.get()
    if button_text == "=":
        try:
            result = str(eval(current))
            entry.delete(0, tk.END)
            entry.insert(tk.END, result)
        except:
            entry.delete(0, tk.END)
            entry.insert(tk.END, "Error")
    elif button_text == "C":
        entry.delete(0, tk.END)
    else:
        entry.insert(tk.END, button_text)


# Create the main window
root = tk.Tk()
root.title("Simple Calculator")

# Set a smaller window size
root.geometry("250x350")  # Width x Height in pixels
root.configure(bg="lightblue")

# Entry widget to display calculations
entry = tk.Entry(root, width=12, font=('Arial', 28), borderwidth=2, relief="solid", justify="right", bg="white")
entry.grid(row=0, column=0, columnspan=4, padx=5, pady=5)

# Button layout (buttons 0-9, +, -, *, /, C, =)
buttons = [
    ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("/", 1, 3),
    ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("*", 2, 3),
    ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("-", 3, 3),
    ("0", 4, 0), ("C", 4, 1), ("=", 4, 2), ("+", 4, 3)
]

# Define button colors
button_color = {
    "default": {"bg": "lightblue", "fg": "black", "activebg": "deepskyblue", "activefg": "white"},
    "operator": {"bg": "lightcoral", "fg": "white", "activebg": "tomato", "activefg": "black"},
    "clear": {"bg": "lightgreen", "fg": "black", "activebg": "darkgreen", "activefg": "white"},
}

# Create and place buttons on the grid (with color settings)
for (text, row, col) in buttons:
    if text in ("+", "-", "*", "/"):
        colors = button_color["operator"]  # Operator button colors
    elif text == "C":
        colors = button_color["clear"]  # Clear button colors
    else:
        colors = button_color["default"]  # Default button colors

    button = tk.Button(
        root, text=text, width=4, height=2, font=('Arial', 12),
        command=lambda t=text: on_click(t),
        bg=colors["bg"], fg=colors["fg"],
        activebackground=colors["activebg"], activeforeground=colors["activefg"],
        padx=5, pady=5  # Add padding for spacing
    )
    button.grid(row=row, column=col, padx=5, pady=5)  # Add padding for spacing

# Start the GUI event loop
root.mainloop()
