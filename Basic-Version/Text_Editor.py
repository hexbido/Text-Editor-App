import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename

# --------------------------------[ File Operations ]-----------------------------------

def open_file():
    """ Opens a file dialog to select and read a text file. """
    filepath = askopenfilename(
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    
    if not filepath:
        return # Exit if no file selected

    # Clear current content and load new text
    text_edit.delete(1.0, tk.END)
    with open(filepath, "r") as input_file:
        text = input_file.read()
        text_edit.insert(tk.END, text)
    
    # Update window title with file path
    window.title(f'Bido Text-Editor - {filepath}')

def save_file():
    """ Opens a save dialog to save the current content to a file. """
    filepath = asksaveasfilename(
        defaultextension="txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    
    if not filepath:
        return # Exit if canceled

    # Write content to the selected file path
    with open(filepath, "w") as output_file:
        text = text_edit.get(1.0, tk.END)
        output_file.write(text)
    
    # Update window title
    window.title(f'Bido Text-Editor - {filepath}')

# --------------------------------[ Main Window Setup ]-----------------------------------

window = tk.Tk()
window.title("Bido Text-Editor")
window.geometry("650x350")

# Configure Grid Layout (Resizable Logic)
window.columnconfigure(0, weight=0) # Sidebar: Fixed width
window.columnconfigure(1, weight=1) # Text Area: Expandable
window.rowconfigure(0, weight=1)    # Row: Expandable

# --------------------------------[ UI Components ]-----------------------------------

# 1. Sidebar Frame
frame_buttons = tk.Frame(window, bg="#e0e0e0", width=150)
frame_buttons.grid(column=0, row=0, sticky="ns")

# 2. Action Buttons
button_open = tk.Button(frame_buttons, text="Open File", command=open_file, bg="white", relief="groove", font=("Arial", 10))
button_save = tk.Button(frame_buttons, text="Save As", command=save_file, bg="white", relief="groove", font=("Arial", 10))

button_open.grid(column=0, row=0, sticky="ew", padx=10, pady=(10, 5))
button_save.grid(column=0, row=1, sticky="ew", padx=10, pady=5)

# 3. Main Text Editor Area
text_edit = tk.Text(window, relief=tk.FLAT, font=("Consolas", 12), highlightthickness=1, highlightbackground="black")
text_edit.grid(column=1, row=0, sticky="nsew", padx=(0, 10), pady=10)

# Configure buttons column to expand horizontally inside the sidebar
frame_buttons.columnconfigure(0, weight=1)

# --------------------------------[ App Loop ]-----------------------------------

window.mainloop()