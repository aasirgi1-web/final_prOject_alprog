# ================= IMPORT MODULE =================
# tkinter      : GUI utama
# ttk          : widget modern (Notebook / Tab)
# filedialog   : dialog buka & simpan file
# messagebox   : popup pesan
# os           : cek file autosave
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os


# ================= KONFIGURASI AUTOSAVE =================
# File untuk menyimpan catatan otomatis
AUTOSAVE_FILE = "autosave_diary.txt"


# ================= BUAT TAB BARU =================
def new_tab():
    # Hitung jumlah tab yang ada
    tab_number = len(notebook.tabs()) + 1

    # Frame sebagai wadah tab
    frame = tk.Frame(notebook)

    # Text area untuk menulis catatan
    text = tk.Text(
        frame,
        font=("Times New Roman", 12),
        wrap="word"
    )
    text.pack(expand=True, fill="both", padx=10, pady=10)

    # Autosave setiap kali mengetik
    text.bind("<KeyRelease>", autosave)

    # Tambahkan tab ke notebook
    notebook.add(frame, text=f"Note {tab_number}")
    notebook.select(frame)

    # Load autosave hanya di tab pertama
    if tab_number == 1:
        load_autosave(text)


# ================= AMBIL TEXT AREA TAB AKTIF =================
def get_current_text():
    current_tab = notebook.select()
    frame = notebook.nametowidget(current_tab)
    return frame.winfo_children()[0]


# ================= AUTOSAVE =================
def autosave(event=None):
    text_area = get_current_text()
    content = text_area.get("1.0", tk.END)

    with open(AUTOSAVE_FILE, "w", encoding="utf-8") as f:
        f.write(content)


# ================= LOAD AUTOSAVE =================
def load_autosave(text_area):
    if os.path.exists(AUTOSAVE_FILE):
        with open(AUTOSAVE_FILE, "r", encoding="utf-8") as f:
            text_area.insert(tk.END, f.read())


# ================= SIMPAN FILE MANUAL =================
def save_note():
    text_area = get_current_text()

    file = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[
            ("Text File", "*.txt"),
            ("Python File", "*.py"),
            ("Markdown", "*.md"),
            ("JSON", "*.json"),
            ("CSV", "*.csv"),
            ("All Files", "*.*")
        ]
    )

    if file:
        with open(file, "w", encoding="utf-8") as f:
            f.write(text_area.get("1.0", tk.END))

        messagebox.showinfo("Info", "Notes saved successfully")


# ================= BUKA FILE TEKS (DAN LAIN-LAIN) =================
def open_note():
    text_area = get_current_text()

    file = filedialog.askopenfilename(
        filetypes=[("All Files", "*.*")]
    )

    if not file:
        return

    text_area.delete("1.0", tk.END)

    try:
        with open(file, "r", encoding="utf-8") as f:
            text_area.insert(tk.END, f.read())

    except UnicodeDecodeError:
        messagebox.showwarning(
            "Warning",
            "File ini bukan file teks dan tidak bisa dibuka"
        )

    except Exception as e:
        messagebox.showerror("Error", str(e))


# ================= HAPUS ISI CATATAN =================
def delete_note():
    text_area = get_current_text()
    text_area.delete("1.0", tk.END)
    autosave()


# ================= TUTUP TAB =================
def close_tab():
    if len(notebook.tabs()) <= 1:
        messagebox.showwarning(
            "Warning",
            "Minimal harus ada 1 tab"
        )
        return

    notebook.forget(notebook.select())
    rename_tabs()


# ================= RENAME TAB AGAR URUT =================
def rename_tabs():
    for index, tab_id in enumerate(notebook.tabs()):
        notebook.tab(tab_id, text=f"Note {index + 1}")


# ================= WINDOW UTAMA =================
root = tk.Tk()
root.title("My Diary Notes")
root.geometry("460x550")


# ================= MENU BAR =================
menubar = tk.Menu(root)

file_menu = tk.Menu(menubar, tearoff=0)
file_menu.add_command(label="Open", command=open_note)
file_menu.add_command(label="Save", command=save_note)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

menubar.add_cascade(label="File", menu=file_menu)
root.config(menu=menubar)


# ================= HEADER =================
header = tk.Frame(root, bg="#4a90e2", height=50)
header.pack(fill="x")

tk.Label(
    header,
    text="My Notes",
    bg="#4a90e2",
    fg="white",
    font=("Arial", 16, "bold")
).pack(pady=10)


# ================= TOOLBAR =================
toolbar = tk.Frame(root)
toolbar.pack(fill="x", pady=5)

tk.Button(toolbar, text="+ New Tab", command=new_tab).pack(side="left", padx=5)
tk.Button(toolbar, text="Close Tab", command=close_tab).pack(side="left", padx=5)
tk.Button(toolbar, text="Delete", command=delete_note).pack(side="left", padx=5)


# ================= NOTEBOOK (TAB SYSTEM) =================
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")


# ================= TAB AWAL =================
new_tab()


# ================= JALANKAN APLIKASI =================
root.mainloop()
