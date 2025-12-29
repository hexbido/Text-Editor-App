import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename

def open_file():
    filepath = askopenfilename(
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if not filepath:
        return
    text_edit.delete(1.0, tk.END)
    with open(filepath, "r") as input_file:
        text = input_file.read()
        text_edit.insert(tk.END, text)
    window.title(f'Bido Text-Editor - {filepath}')
    
def save_file():
    filepath = asksaveasfilename(
        defaultextension="txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if not filepath:
        return
    with open(filepath, "w") as output_file:
        text = text_edit.get(1.0, tk.END)
        output_file.write(text)
    window.title(f'Bido Text-Editor - {filepath}')

window = tk.Tk()
window.title("Bido Text-Editor")
window.geometry("650x350")

window.columnconfigure(0, weight=0)
window.columnconfigure(1, weight=1)
window.rowconfigure(0, weight=1)

frame_buttons = tk.Frame(window, bg="#e0e0e0", width=150)

button_open = tk.Button(frame_buttons, text="Open File", command=open_file, bg="white", relief="groove", font=("Arial", 10))
button_save = tk.Button(frame_buttons, text="Save As", command=save_file, bg="white", relief="groove", font=("Arial", 10))

button_open.grid(column=0, row=0, sticky="ew", padx=10, pady=(10, 5))
button_save.grid(column=0, row=1, sticky="ew", padx=10, pady=5)

text_edit = tk.Text(window, relief=tk.FLAT, font=("Consolas", 12), highlightthickness=1, highlightbackground="black")
frame_buttons.grid(column=0, row=0, sticky="ns")

text_edit.grid(column=1, row=0, sticky="nsew", padx=(0, 10), pady=10)
frame_buttons.columnconfigure(0, weight=1)

window.mainloop()