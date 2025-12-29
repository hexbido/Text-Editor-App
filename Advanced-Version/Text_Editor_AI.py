import tkinter as tk
from tkinter import filedialog, messagebox
import os

class CodeEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Bido Code Editor"); self.geometry("700x350")
        self.dark, self.side_on, self.curr_dir = True, True, os.getcwd()
        self.colors = { # Smart Color Configuration
            True: {"bg": "#282c34", "side": "#21252b", "fg": "#abb2bf", "sel": "#3e4451", "cur": "white"},
            False: {"bg": "white", "side": "#f3f3f3", "fg": "#383a42", "sel": "#e5e5e6", "cur": "black"}
        }
        self.columnconfigure(1, weight=1); self.rowconfigure(2, weight=1)
        self.setup_ui(); self.setup_shortcuts(); self.apply_theme(); self.refresh_dir()

    def setup_ui(self):
        # Menu
        menubar = tk.Menu(self)
        f_menu = tk.Menu(menubar, tearoff=0); v_menu = tk.Menu(menubar, tearoff=0)
        for lbl, cmd, acc in [("New File", self.new_file, "Ctrl+N"), ("Open File", self.open_file, "Ctrl+O"), ("Save", self.save_file, "Ctrl+S"), ("Delete File", self.del_file, "Ctrl+D")]:
            f_menu.add_command(label=lbl, accelerator=acc, command=cmd)
        f_menu.add_separator(); f_menu.add_command(label="Exit", command=self.quit)
        v_menu.add_command(label="Toggle Theme 🌗", command=self.toggle_theme)
        v_menu.add_command(label="Toggle Sidebar ☰", command=self.toggle_side)
        menubar.add_cascade(label="File", menu=f_menu); menubar.add_cascade(label="View", menu=v_menu)
        self.config(menu=menubar)

        # Toolbar
        self.bar = tk.Frame(self, height=30); self.bar.grid(row=0, column=0, columnspan=2, sticky="ew")
        self.btn_side = tk.Button(self.bar, text="☰", command=self.toggle_side, width=4, relief="flat", font=("Segoe UI", 10))
        self.btn_side.pack(side="left", padx=5, pady=2)
        self.lbl_head = tk.Label(self.bar, text="Bido Editor", font=("Segoe UI", 9, "bold")); self.lbl_head.pack(side="left", padx=10)

        # Sidebar
        self.side = tk.Frame(self, width=220); self.side.grid(row=1, column=0, rowspan=2, sticky="ns"); self.side.pack_propagate(0)
        self.btn_open = tk.Button(self.side, text="OPEN FOLDER", command=self.load_dir, relief="flat", anchor="w", padx=10, font=("Segoe UI", 8, "bold"))
        self.btn_open.pack(fill="x", pady=(10, 2))
        self.btn_save = tk.Button(self.side, text="SAVE AS...", command=self.save_file, relief="flat", anchor="w", padx=10, font=("Segoe UI", 8, "bold"))
        self.btn_save.pack(fill="x", pady=(0, 10))
        self.lbl_exp = tk.Label(self.side, text="EXPLORER", font=("Segoe UI", 8, "bold"), anchor="w", padx=10); self.lbl_exp.pack(fill="x")
        
        self.lst = tk.Listbox(self.side, relief="flat", bd=0, font=("Segoe UI", 10), activestyle="none")
        self.lst.pack(fill="both", expand=True, padx=0, pady=5); self.lst.bind("<Double-Button-1>", self.open_side)

        # Editor & Status
        self.txt = tk.Text(self, font=("Consolas", 13), undo=True, wrap="none", relief="flat", padx=10, pady=10)
        self.txt.grid(row=1, column=1, rowspan=2, sticky="nsew"); self.txt.bind("<KeyRelease>", self.update_stat)
        self.scr = tk.Scrollbar(self, command=self.txt.yview); self.scr.grid(row=1, column=2, rowspan=2, sticky="ns")
        self.txt.config(yscrollcommand=self.scr.set)
        
        self.stat = tk.Label(self, text="Ready", anchor="e", padx=10, font=("Segoe UI", 9))
        self.stat.grid(row=3, column=0, columnspan=3, sticky="ew")

    def setup_shortcuts(self):
        for k, f in [("<Control-n>", self.new_file), ("<Control-o>", self.open_file), ("<Control-s>", self.save_file), ("<Control-d>", self.del_file)]:
            self.bind(k, lambda e, func=f: func())

    def apply_theme(self):
        c = self.colors[self.dark]
        self.config(bg=c["bg"])
        self.bar.config(bg=c["side"]); self.lbl_head.config(bg=c["side"], fg=c["fg"]); self.btn_side.config(bg=c["side"], fg=c["fg"])
        self.side.config(bg=c["side"]); self.btn_open.config(bg=c["side"], fg=c["fg"]); self.btn_save.config(bg=c["side"], fg=c["fg"])
        self.lbl_exp.config(bg=c["side"], fg=c["fg"]); self.lst.config(bg=c["side"], fg=c["fg"], selectbackground=c["sel"], selectforeground=c["fg"])
        self.txt.config(bg=c["bg"], fg=c["fg"], insertbackground=c["cur"], selectbackground=c["sel"])
        self.stat.config(bg=c["side"], fg=c["fg"])

    def toggle_theme(self): self.dark = not self.dark; self.apply_theme()
    def toggle_side(self): self.side.grid_remove() if self.side.winfo_viewable() else self.side.grid()
    def update_stat(self, e=None): self.stat.config(text=f"Ln: {self.txt.index(tk.INSERT).split('.')[0]} Col: {self.txt.index(tk.INSERT).split('.')[1]}")

    def load_dir(self):
        d = filedialog.askdirectory()
        if d: self.curr_dir = d; self.refresh_dir()

    def refresh_dir(self):
        self.lst.delete(0, tk.END)
        try: [self.lst.insert(tk.END, f) for f in os.listdir(self.curr_dir) if os.path.isfile(os.path.join(self.curr_dir, f))]
        except: pass

    def new_file(self):
        self.txt.delete(1.0, tk.END); name, c = "untitled.txt", 1
        while os.path.exists(os.path.join(self.curr_dir, name)): name, c = f"untitled_{c}.txt", c+1
        with open(os.path.join(self.curr_dir, name), "w") as f: f.write("")
        self.refresh_dir(); self.title(f"Bido Editor - {name}")

    def open_file(self):
        p = filedialog.askopenfilename(filetypes=[("All", "*.*")])
        if p:
            self.txt.delete(1.0, tk.END); self.txt.insert(1.0, open(p, "r", encoding="utf-8").read())
            self.title(f"Bido Editor - {p}")

    def open_side(self, e):
        try: self.open_logic(os.path.join(self.curr_dir, self.lst.get(self.lst.curselection())))
        except: pass

    def open_logic(self, p):
        self.txt.delete(1.0, tk.END); self.txt.insert(1.0, open(p, "r", encoding="utf-8").read())
        self.title(f"Bido Editor - {p}"); self.update_stat()

    def save_file(self):
        p = filedialog.asksaveasfilename(defaultextension=".txt")
        if p: 
            with open(p, "w", encoding="utf-8") as f: f.write(self.txt.get(1.0, tk.END))
            self.title(f"Bido Editor - {p}")

    def del_file(self):
        try:
            fn = self.lst.get(self.lst.curselection())
            if messagebox.askyesno("Delete", f"Are You Sure You Want Delete '{fn}'?"):
                os.remove(os.path.join(self.curr_dir, fn)); self.txt.delete(1.0, tk.END); self.refresh_dir()
        except: messagebox.showwarning("Info", "Select file first")

if __name__ == "__main__":
    CodeEditor().mainloop()