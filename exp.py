import tkinter as tk

def on_button_click():
    root.user_clicked.set(True)

root = tk.Tk()

# Create a button to signal the user click
button = tk.Button(root, text="Continue", command=on_button_click)
button.pack()

# Variable to track if the user has clicked
root.user_clicked = tk.BooleanVar(value=False)

# Wait until the user clicks the button
root.wait_variable(root.user_clicked)

# Code execution will continue here after the button is clicked
print("Button clicked!")

root.mainloop()
