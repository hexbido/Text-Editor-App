import tkinter as tk
from tkinter import filedialog, messagebox
import os

# --------------------------------[ Configuration ]-----------------------------------

# Default Directory
DEFAULT_DIR = os.getcwd()

# Color Palettes (Dark & Light Modes)
THEMES = {
    True: {  # Dark Mode
        "bg": "#282c34", "fg": "#abb2bf", 
        "side": "#21252b", "sel": "#3e4451", "cur": "white"
    },
    False: { # Light Mode
        "bg": "#ffffff", "fg": "#383a42", 
        "side": "#f0f0f0", "sel": "#e5e5e6", "cur": "black"
    }
}

# --------------------------------[ Main Application ]-----------------------------------

class CodeEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Window Setup
        self.title("Bido Code Editor")
        self.geometry("700x350")
        
        # State Variables
        self.is_dark_mode = True
        self.current_dir = DEFAULT_DIR
        
        # Configure Grid Layout
        self.columnconfigure(1, weight=1) # Text area expands
        self.rowconfigure(2, weight=1)    # Vertical expansion
        
        # Build Interface
        self.setup_ui()
        self.setup_shortcuts()
        self.apply_theme()
        self.refresh_directory()

    # --------------------------------[ UI Construction ]-----------------------------------

    def setup_ui(self):
        # 1. Main Menu Bar
        menubar = tk.Menu(self)
        
        # File Menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New File", accelerator="Ctrl+N", command=self.new_file)
        file_menu.add_command(label="Open File", accelerator="Ctrl+O", command=self.open_file_dialog)
        file_menu.add_command(label="Save File", accelerator="Ctrl+S", command=self.save_file)
        file_menu.add_command(label="Delete File", accelerator="Ctrl+D", command=self.delete_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        
        # View Menu
        view_menu = tk.Menu(menubar, tearoff=0)
        view_menu.add_command(label="Toggle Theme 🌗", command=self.toggle_theme)
        view_menu.add_command(label="Toggle Sidebar ☰", command=self.toggle_sidebar)
        
        menubar.add_cascade(label="File", menu=file_menu)
        menubar.add_cascade(label="View", menu=view_menu)
        self.config(menu=menubar)

        # 2. Top Toolbar
        self.toolbar = tk.Frame(self, height=30)
        self.toolbar.grid(row=0, column=0, columnspan=2, sticky="ew")
        
        self.btn_toggle = tk.Button(self.toolbar, text="☰", command=self.toggle_sidebar, width=4, relief="flat", font=("Segoe UI", 10))
        self.btn_toggle.pack(side="left", padx=5, pady=2)
        
        self.lbl_title = tk.Label(self.toolbar, text="Bido Editor", font=("Segoe UI", 9, "bold"))
        self.lbl_title.pack(side="left", padx=10)

        # 3. Sidebar (Explorer)
        self.sidebar = tk.Frame(self, width=220)
        self.sidebar.grid(row=1, column=0, rowspan=2, sticky="ns")
        self.sidebar.pack_propagate(False) # Force width
        
        self.btn_open_folder = tk.Button(self.sidebar, text="OPEN FOLDER", command=self.change_directory, relief="flat", anchor="w", padx=10, font=("Segoe UI", 8, "bold"))
        self.btn_open_folder.pack(fill="x", pady=(10, 2))
        
        self.lbl_explorer = tk.Label(self.sidebar, text="EXPLORER", font=("Segoe UI", 8, "bold"), anchor="w", padx=10)
        self.lbl_explorer.pack(fill="x")
        
        self.file_listbox = tk.Listbox(self.sidebar, relief="flat", bd=0, font=("Segoe UI", 10), activestyle="none")
        self.file_listbox.pack(fill="both", expand=True, padx=5, pady=5)
        self.file_listbox.bind("<Double-Button-1>", self.on_sidebar_click)

        # 4. Text Editor Area
        self.text_area = tk.Text(self, font=("Consolas", 13), undo=True, wrap="none", relief="flat", padx=10, pady=10)
        self.text_area.grid(row=1, column=1, rowspan=2, sticky="nsew")
        self.text_area.bind("<KeyRelease>", self.update_status)
        
        # Scrollbar
        self.scrollbar = tk.Scrollbar(self, command=self.text_area.yview)
        self.scrollbar.grid(row=1, column=2, rowspan=2, sticky="ns")
        self.text_area.config(yscrollcommand=self.scrollbar.set)
        
        # 5. Status Bar
        self.status_bar = tk.Label(self, text="Ready", anchor="e", padx=10, font=("Segoe UI", 9))
        self.status_bar.grid(row=3, column=0, columnspan=3, sticky="ew")

    def setup_shortcuts(self):
        self.bind("<Control-n>", lambda e: self.new_file())
        self.bind("<Control-o>", lambda e: self.open_file_dialog())
        self.bind("<Control-s>", lambda e: self.save_file())
        self.bind("<Control-d>", lambda e: self.delete_file())

    # --------------------------------[ Theme & Logic ]-----------------------------------

    def apply_theme(self):
        # Apply Colors Based On Current Mode
        colors = THEMES[self.is_dark_mode]
        
        self.config(bg=colors["bg"])
        
        # Toolbar Styling
        self.toolbar.config(bg=colors["side"])
        self.lbl_title.config(bg=colors["side"], fg=colors["fg"])
        self.btn_toggle.config(bg=colors["side"], fg=colors["fg"])
        
        # Sidebar Styling
        self.sidebar.config(bg=colors["side"])
        self.btn_open_folder.config(bg=colors["side"], fg=colors["fg"])
        self.lbl_explorer.config(bg=colors["side"], fg=colors["fg"])
        self.file_listbox.config(bg=colors["side"], fg=colors["fg"], selectbackground=colors["sel"], selectforeground=colors["fg"])
        
        # Editor Styling
        self.text_area.config(bg=colors["bg"], fg=colors["fg"], insertbackground=colors["cur"], selectbackground=colors["sel"])
        self.status_bar.config(bg=colors["side"], fg=colors["fg"])

    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        self.apply_theme()

    def toggle_sidebar(self):
        if self.sidebar.winfo_viewable():
            self.sidebar.grid_remove()
        else:
            self.sidebar.grid()

    def update_status(self, event=None):
        # Update Cursor Position In Status Bar
        cursor_pos = self.text_area.index(tk.INSERT).split('.')
        self.status_bar.config(text=f"Ln: {cursor_pos[0]} Col: {cursor_pos[1]}")

    # --------------------------------[ File Operations ]-----------------------------------

    def change_directory(self):
        path = filedialog.askdirectory()
        if path:
            self.current_dir = path
            self.refresh_directory()

    def refresh_directory(self):
        self.file_listbox.delete(0, tk.END)
        try:
            files = sorted([f for f in os.listdir(self.current_dir) if os.path.isfile(os.path.join(self.current_dir, f))])
            for f in files:
                self.file_listbox.insert(tk.END, f)
        except Exception as e:
            print(e)

    def new_file(self):
        self.text_area.delete(1.0, tk.END)
        name, count = "untitled.txt", 1
        
        # Create unique name
        while os.path.exists(os.path.join(self.current_dir, name)):
            name, count = f"untitled_{count}.txt", count + 1
        
        # Create empty file immediately (as per Explorer logic)
        with open(os.path.join(self.current_dir, name), "w") as f:
            f.write("")
            
        self.refresh_directory()
        self.title(f"Bido Editor - {name}")

    def open_file_dialog(self):
        path = filedialog.askopenfilename(filetypes=[("All Files", "*.*")])
        if path:
            self.load_file_content(path)

    def on_sidebar_click(self, event):
        try:
            selection = self.file_listbox.curselection()
            if selection:
                filename = self.file_listbox.get(selection[0])
                full_path = os.path.join(self.current_dir, filename)
                self.load_file_content(full_path)
        except Exception:
            pass

    def load_file_content(self, path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(1.0, content)
            self.title(f"Bido Editor - {path}")
            self.update_status()
        except Exception as e:
            messagebox.showerror("Error", f"Could not open file: {e}")

    def save_file(self):
        path = filedialog.asksaveasfilename(defaultextension=".txt", initialdir=self.current_dir)
        if path:
            try:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(self.text_area.get(1.0, tk.END))
                self.title(f"Bido Editor - {path}")
                self.refresh_directory()
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file: {e}")

    def delete_file(self):
        try:
            selection = self.file_listbox.curselection()
            if not selection:
                messagebox.showwarning("Info", "Select a file from the sidebar first.")
                return

            filename = self.file_listbox.get(selection[0])
            if messagebox.askyesno("Delete", f"Are you sure you want to delete '{filename}'?"):
                os.remove(os.path.join(self.current_dir, filename))
                self.text_area.delete(1.0, tk.END)
                self.refresh_directory()
        except Exception as e:
            messagebox.showerror("Error", f"Could not delete file: {e}")

if __name__ == "__main__":
    CodeEditor().mainloop()