import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# ==========================================================
# KONFIGURASI
# ==========================================================

CONFIG_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "config.json"
)

# ==========================================================
# WARNA TEMA (Dark Mode)
# ==========================================================

BG_COLOR = "#0D1117"
CARD_COLOR = "#1A1F2E"
ACCENT_COLOR = "#2196F3"
TEXT_COLOR = "#E6EDF3"
TEXT_SECONDARY = "#8B949E"

# ==========================================================
# FUNGSI BACA/SIMPAN CONFIG
# ==========================================================

def load_config():
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error baca config: {e}")
        return {"profiles": {}}

def save_config(config):
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error simpan config: {e}")
        return False

# ==========================================================
# APLIKASI UTAMA
# ==========================================================

class DashboardSettings:
    def __init__(self, root):
        self.root = root
        self.root.title("Hafz Dashboard Settings")
        self.root.geometry("900x600")
        self.root.configure(bg=BG_COLOR)
        
        self.config = load_config()
        self.current_profile = "default"
        
        self.setup_ui()
        self.refresh_profile_list()
        self.refresh_button_list()
    
    def setup_ui(self):
        header = tk.Frame(self.root, bg=CARD_COLOR, height=60)
        header.pack(fill="x", padx=10, pady=10)
        header.pack_propagate(False)
        
        title = tk.Label(
            header,
            text="🎯 HAFZ DASHBOARD SETTINGS",
            font=("Segoe UI", 16, "bold"),
            bg=CARD_COLOR,
            fg=TEXT_COLOR
        )
        title.pack(side="left", padx=20)
        
        main = tk.Frame(self.root, bg=BG_COLOR)
        main.pack(fill="both", expand=True, padx=10, pady=10)
        
        left = tk.Frame(main, bg=CARD_COLOR, width=200)
        left.pack(side="left", fill="y", padx=(0, 10))
        left.pack_propagate(False)
        
        tk.Label(
            left,
            text="Profiles",
            font=("Segoe UI", 12, "bold"),
            bg=CARD_COLOR,
            fg=TEXT_COLOR
        ).pack(pady=10)
        
        self.profile_listbox = tk.Listbox(
            left,
            bg=CARD_COLOR,
            fg=TEXT_COLOR,
            selectbackground=ACCENT_COLOR,
            font=("Segoe UI", 10),
            borderwidth=0,
            highlightthickness=0
        )
        self.profile_listbox.pack(fill="both", expand=True, padx=10, pady=10)
        self.profile_listbox.bind("<<ListboxSelect>>", self.on_profile_select)
        
        center = tk.Frame(main, bg=CARD_COLOR)
        center.pack(side="left", fill="both", expand=True)
        
        tk.Label(
            center,
            text="Buttons",
            font=("Segoe UI", 12, "bold"),
            bg=CARD_COLOR,
            fg=TEXT_COLOR
        ).pack(pady=10)
        
        columns = ("icon", "label", "endpoint", "color")
        self.button_tree = ttk.Treeview(
            center,
            columns=columns,
            show="headings",
            height=15
        )
        self.button_tree.heading("icon", text="Icon")
        self.button_tree.heading("label", text="Label")
        self.button_tree.heading("endpoint", text="Endpoint")
        self.button_tree.heading("color", text="Color")
        self.button_tree.column("icon", width=100)
        self.button_tree.column("label", width=150)
        self.button_tree.column("endpoint", width=200)
        self.button_tree.column("color", width=100)
        self.button_tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        btn_frame = tk.Frame(center, bg=CARD_COLOR)
        btn_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Button(
            btn_frame,
            text="➕ Tambah",
            command=self.add_button,
            bg=ACCENT_COLOR,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padx=20,
            pady=5
        ).pack(side="left", padx=5)
        
        tk.Button(
            btn_frame,
            text="✏️ Edit",
            command=self.edit_button,
            bg="#FF9800",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padx=20,
            pady=5
        ).pack(side="left", padx=5)
        
        tk.Button(
            btn_frame,
            text="🗑️ Hapus",
            command=self.delete_button,
            bg="#F44336",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padx=20,
            pady=5
        ).pack(side="left", padx=5)
        
        tk.Button(
            btn_frame,
            text="💾 Simpan",
            command=self.save_all,
            bg="#4CAF50",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padx=20,
            pady=5
        ).pack(side="right", padx=5)
    
    def refresh_profile_list(self):
        self.profile_listbox.delete(0, tk.END)
        for profile_name in self.config.get("profiles", {}).keys():
            self.profile_listbox.insert(tk.END, profile_name)
        
        if "default" in self.config.get("profiles", {}):
            self.profile_listbox.selection_set(0)
    
    def refresh_button_list(self):
        for item in self.button_tree.get_children():
            self.button_tree.delete(item)
        
        buttons = self.config.get("profiles", {}).get(self.current_profile, [])
        
        for btn in buttons:
            self.button_tree.insert(
                "",
                "end",
                values=(
                    btn.get("icon", ""),
                    btn.get("label", ""),
                    btn.get("endpoint", ""),
                    btn.get("color", "")
                )
            )
    
    def on_profile_select(self, event):
        selection = self.profile_listbox.curselection()
        if selection:
            self.current_profile = self.profile_listbox.get(selection[0])
            self.refresh_button_list()
    
    def add_button(self):
        dialog = ButtonDialog(self.root, "Tambah Tombol")
        self.root.wait_window(dialog.dialog)
        
        if dialog.result:
            if self.current_profile not in self.config["profiles"]:
                self.config["profiles"][self.current_profile] = []
            
            self.config["profiles"][self.current_profile].append(dialog.result)
            self.refresh_button_list()
            messagebox.showinfo("Sukses", "Tombol ditambahkan! Klik 'Simpan' untuk menyimpan.")
    
    def edit_button(self):
        selection = self.button_tree.selection()
        if not selection:
            messagebox.showwarning("Peringatan", "Pilih tombol yang mau diedit!")
            return
        
        item = self.button_tree.item(selection[0])
        values = item["values"]
        
        old_button = {
            "icon": values[0],
            "label": values[1],
            "endpoint": values[2],
            "color": values[3]
        }
        
        dialog = ButtonDialog(self.root, "Edit Tombol", old_button)
        self.root.wait_window(dialog.dialog)
        
        if dialog.result:
            buttons = self.config["profiles"][self.current_profile]
            index = self.button_tree.index(selection[0])
            buttons[index] = dialog.result
            self.refresh_button_list()
            messagebox.showinfo("Sukses", "Tombol diedit! Klik 'Simpan' untuk menyimpan.")
    
    def delete_button(self):
        selection = self.button_tree.selection()
        if not selection:
            messagebox.showwarning("Peringatan", "Pilih tombol yang mau dihapus!")
            return
        
        if messagebox.askyesno("Konfirmasi", "Yakin mau hapus tombol ini?"):
            index = self.button_tree.index(selection[0])
            del self.config["profiles"][self.current_profile][index]
            self.refresh_button_list()
            messagebox.showinfo("Sukses", "Tombol dihapus! Klik 'Simpan' untuk menyimpan.")
    
    def save_all(self):
        if save_config(self.config):
            messagebox.showinfo("Sukses", "Config berhasil disimpan!")
        else:
            messagebox.showerror("Error", "Gagal menyimpan config!")

# ==========================================================
# DIALOG TAMBAH/EDIT TOMBOL
# ==========================================================

class ButtonDialog:
    def __init__(self, parent, title, button_data=None):
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("400x350")
        self.dialog.configure(bg=BG_COLOR)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - 200
        y = (self.dialog.winfo_screenheight() // 2) - 175
        self.dialog.geometry(f"+{x}+{y}")
        
        form = tk.Frame(self.dialog, bg=BG_COLOR)
        form.pack(fill="both", expand=True, padx=20, pady=20)
        
        tk.Label(form, text="Icon:", bg=BG_COLOR, fg=TEXT_COLOR, font=("Segoe UI", 10)).grid(row=0, column=0, sticky="w", pady=5)
        self.icon_entry = tk.Entry(form, font=("Segoe UI", 10), width=30)
        self.icon_entry.grid(row=0, column=1, pady=5, padx=10)
        
        tk.Label(form, text="Label:", bg=BG_COLOR, fg=TEXT_COLOR, font=("Segoe UI", 10)).grid(row=1, column=0, sticky="w", pady=5)
        self.label_entry = tk.Entry(form, font=("Segoe UI", 10), width=30)
        self.label_entry.grid(row=1, column=1, pady=5, padx=10)
        
        tk.Label(form, text="Endpoint:", bg=BG_COLOR, fg=TEXT_COLOR, font=("Segoe UI", 10)).grid(row=2, column=0, sticky="w", pady=5)
        self.endpoint_entry = tk.Entry(form, font=("Segoe UI", 10), width=30)
        self.endpoint_entry.grid(row=2, column=1, pady=5, padx=10)
        
        tk.Label(form, text="Color:", bg=BG_COLOR, fg=TEXT_COLOR, font=("Segoe UI", 10)).grid(row=3, column=0, sticky="w", pady=5)
        self.color_var = tk.StringVar(value="blue")
        color_combo = ttk.Combobox(
            form,
            textvariable=self.color_var,
            values=["green", "blue", "purple", "orange", "red", "cyan"],
            state="readonly",
            font=("Segoe UI", 10),
            width=28
        )
        color_combo.grid(row=3, column=1, pady=5, padx=10)
        
        if button_data:
            self.icon_entry.insert(0, button_data.get("icon", ""))
            self.label_entry.insert(0, button_data.get("label", ""))
            self.endpoint_entry.insert(0, button_data.get("endpoint", ""))
            self.color_var.set(button_data.get("color", "blue"))
        
        btn_frame = tk.Frame(self.dialog, bg=BG_COLOR)
        btn_frame.pack(fill="x", padx=20, pady=20)
        
        tk.Button(
            btn_frame,
            text="💾 Simpan",
            command=self.save,
            bg="#4CAF50",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padx=20,
            pady=5
        ).pack(side="right", padx=5)
        
        tk.Button(
            btn_frame,
            text="❌ Batal",
            command=self.dialog.destroy,
            bg="#F44336",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padx=20,
            pady=5
        ).pack(side="right", padx=5)
    
    def save(self):
        icon = self.icon_entry.get().strip()
        label = self.label_entry.get().strip()
        endpoint = self.endpoint_entry.get().strip()
        color = self.color_var.get()
        
        if not icon or not label or not endpoint:
            messagebox.showwarning("Peringatan", "Semua field harus diisi!")
            return
        
        self.result = {
            "icon": icon,
            "label": label,
            "endpoint": endpoint,
            "color": color
        }
        self.dialog.destroy()

# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":
    root = tk.Tk()
    app = DashboardSettings(root)
    root.mainloop()