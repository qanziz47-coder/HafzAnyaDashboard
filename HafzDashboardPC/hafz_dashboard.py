import tkinter as tk
from tkinter import ttk, messagebox
import threading
import json
import subprocess
import os
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

# ==========================================================
# KONFIGURASI
# ==========================================================

HOST = "0.0.0.0"
PORT = 5000

CONFIG_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "config.json"
)

DRAWABLE_PATH = r"C:\Users\zankx\AndroidStudioProjects\HafzAnyaDashboard\app\src\main\res\drawable"

# ==========================================================
# WARNA TEMA (Dark Mode)
# ==========================================================

BG_COLOR = "#0D1117"
CARD_COLOR = "#1A1F2E"
ACCENT_COLOR = "#2196F3"
TEXT_COLOR = "#E6EDF3"
TEXT_SECONDARY = "#8B949E"
SUCCESS_COLOR = "#4CAF50"
DANGER_COLOR = "#F44336"
WARNING_COLOR = "#FF9800"

# ==========================================================
# FUNGSI BACA/SIMPAN CONFIG
# ==========================================================

config_lock = threading.Lock()

def load_config():
    """Baca config.json"""
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error baca config: {e}")
        return {"profiles": {}, "bottom_buttons": []}

def save_config(config):
    """Simpan config.json"""
    with config_lock:
        try:
            with open(CONFIG_PATH, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error simpan config: {e}")
            return False

# ==========================================================
# FUNGSI DETEKSI APLIKASI AKTIF
# ==========================================================

def get_active_app():
    """Deteksi aplikasi yang sedang aktif di PC"""
    try:
        ps_command = (
            "Add-Type @'\n"
            "using System;\n"
            "using System.Runtime.InteropServices;\n"
            "public class Win32 {\n"
            "    [DllImport(\"user32.dll\")]\n"
            "    public static extern IntPtr GetForegroundWindow();\n"
            "    [DllImport(\"user32.dll\")]\n"
            "    public static extern uint GetWindowThreadProcessId(IntPtr hWnd, out uint processId);\n"
            "}\n"
            "'@\n"
            "$hwnd = [Win32]::GetForegroundWindow()\n"
            "[uint32]$processId = 0\n"
            "[Win32]::GetWindowThreadProcessId($hwnd, [ref]$processId) | Out-Null\n"
            "$proc = Get-Process -Id $processId\n"
            "Write-Output $proc.ProcessName"
        )
        
        result = subprocess.run(
            ["powershell", "-Command", ps_command],
            capture_output=True, text=True, timeout=5
        )
        
        return result.stdout.strip()
        
    except Exception as e:
        print(f"Error deteksi app: {e}")
        return ""

# ==========================================================
# MAPPING APLIKASI → PROFIL
# ==========================================================

APP_PROFILES = {
    "spotify": "spotify",
    "chrome": "chrome",
    "firefox": "browser",
    "msedge": "browser",
    "discord": "discord",
    "steam": "gaming",
    "code": "vscode",
    "explorer": "files",
    "notepad": "notepad",
    "calc": "calculator",
    "taskmgr": "taskmgr",
    "cmd": "cmd",
    "windowsterminal": "cmd",
    "powershell": "cmd",
    "vlc": "vlc",
    "winword": "word",
    "excel": "excel",
    "studio64": "android-studio",
}

def get_profile_for_app(app_name):
    """Mapping nama aplikasi ke profil"""
    if not app_name:
        return "default"
    
    app_lower = app_name.lower().strip()
    
    for key, profile in APP_PROFILES.items():
        if key.lower() == app_lower:
            return profile
    
    for key, profile in APP_PROFILES.items():
        if key.lower() in app_lower or app_lower in key.lower():
            return profile
    
    return "default"

# ==========================================================
# HANDLER HTTP
# ==========================================================

class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        print(f"[SERVER] Menerima request: {self.path}")

        # SPOTIFY
        if self.path == "/spotify":
            try:
                os.startfile("spotify:")
                self._send_ok(b"Spotify dibuka")
            except Exception as e:
                self._send_error(f"Gagal buka Spotify: {e}")

        # CHROME
        elif self.path == "/chrome":
            try:
                chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
                subprocess.Popen([chrome_path])
                self._send_ok(b"Chrome dibuka")
            except Exception as e:
                self._send_error(f"Gagal buka Chrome: {e}")

        # FILE EXPLORER
        elif self.path == "/file":
            try:
                subprocess.Popen(["explorer", "C:\\"])
                self._send_ok(b"File Explorer dibuka")
            except Exception as e:
                self._send_error(f"Gagal buka File Explorer: {e}")

        # WHATSAPP
        elif self.path == "/whatsapp":
            try:
                os.startfile("whatsapp://")
                self._send_ok(b"WhatsApp dibuka")
            except Exception as e:
                self._send_error(f"Gagal buka WhatsApp: {e}")

        # SHUTDOWN
        elif self.path == "/shutdown":
            try:
                subprocess.Popen(["shutdown", "/s", "/t", "10"])
                self._send_ok(b"Shutdown dalam 10 detik")
            except Exception as e:
                self._send_error(f"Gagal shutdown: {e}")

        # RESTART
        elif self.path == "/restart":
            try:
                subprocess.Popen(["shutdown", "/r", "/t", "10"])
                self._send_ok(b"Restart dalam 10 detik")
            except Exception as e:
                self._send_error(f"Gagal restart: {e}")

        # LOCK
        elif self.path == "/lock":
            try:
                subprocess.Popen(["rundll32.exe", "user32.dll,LockWorkStation"])
                self._send_ok(b"PC dikunci")
            except Exception as e:
                self._send_error(f"Gagal lock: {e}")

        # CMD
        elif self.path == "/cmd":
            try:
                subprocess.Popen(
                    "start cmd.exe",
                    shell=True,
                    creationflags=subprocess.CREATE_NEW_CONSOLE
                )
                self._send_ok(b"CMD dibuka")
            except Exception as e:
                self._send_error(f"Gagal buka CMD: {e}")

        # CALCULATOR
        elif self.path == "/calc":
            try:
                subprocess.Popen("start calc.exe", shell=True)
                self._send_ok(b"Calculator dibuka")
            except Exception as e:
                self._send_error(f"Gagal buka Calculator: {e}")

        # TASK MANAGER
        elif self.path == "/taskmgr":
            try:
                subprocess.Popen("start taskmgr.exe", shell=True)
                self._send_ok(b"Task Manager dibuka")
            except Exception as e:
                self._send_error(f"Gagal buka Task Manager: {e}")

        # SLEEP
        elif self.path == "/sleep":
            try:
                subprocess.Popen(["rundll32.exe", "powrprof.dll,SetSuspendState", "0,1,0"])
                self._send_ok(b"PC sleep")
            except Exception as e:
                self._send_error(f"Gagal sleep: {e}")

        # SETTINGS
        elif self.path == "/settings":
            try:
                subprocess.Popen(["start", "ms-settings:"], shell=True)
                self._send_ok(b"Settings dibuka")
            except Exception as e:
                self._send_error(f"Gagal buka Settings: {e}")

        # STATS
        elif self.path == "/stats":
            try:
                cpu_result = subprocess.run(
                    ["powershell", "-Command",
                     "(Get-CimInstance Win32_Processor).LoadPercentage"],
                    capture_output=True, text=True, timeout=5
                )
                cpu = int(cpu_result.stdout.strip() or 0)

                ram_result = subprocess.run(
                    ["powershell", "-Command",
                     "$os = Get-CimInstance Win32_OperatingSystem; "
                     "[math]::Round(($os.TotalVisibleMemorySize - $os.FreePhysicalMemory) / $os.TotalVisibleMemorySize * 100)"],
                    capture_output=True, text=True, timeout=5
                )
                ram = int(ram_result.stdout.strip() or 0)

                response = json.dumps({"cpu": cpu, "ram": ram})
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(response.encode())
            except Exception as e:
                self._send_error(f"Gagal baca stats: {e}")

        # UPTIME
        elif self.path == "/uptime":
            try:
                result = subprocess.run(
                    ["powershell", "-Command",
                     "$boot = (Get-CimInstance Win32_OperatingSystem).LastBootUpTime; "
                     "$uptime = (Get-Date) - $boot; "
                     "$totalMinutes = [math]::Floor($uptime.TotalMinutes); "
                     "$hours = [math]::Floor($totalMinutes / 60); "
                     "$minutes = $totalMinutes % 60; "
                     "Write-Output \"$hours`:$minutes\""],
                    capture_output=True, text=True, timeout=10
                )
                
                uptime_str = result.stdout.strip()
                
                if not uptime_str:
                    uptime_str = "0:0"
                
                response = json.dumps({"uptime": uptime_str})
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(response.encode())
            except Exception as e:
                response = json.dumps({"uptime": "0:0"})
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(response.encode())

        # ACTIVE APP
        elif self.path == "/active-app":
            try:
                app_name = get_active_app()
                profile = get_profile_for_app(app_name)
                
                response = json.dumps({
                    "app": app_name,
                    "profile": profile
                })
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(response.encode())
            except Exception as e:
                response = json.dumps({"app": "", "profile": "default"})
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(response.encode())

        # PROFILES (BACA DARI config.json)
        elif self.path == "/profiles":
            try:
                config = load_config()
                profiles = config.get("profiles", {})
                
                response = json.dumps(profiles)
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(response.encode())
            except Exception as e:
                self._send_error(f"Gagal kirim profiles: {e}")

        # ==================================================
        # BOTTOM BUTTONS (Tombol Bawah)
        # ==================================================
        elif self.path == "/bottom-buttons":
            try:
                config = load_config()
                bottom = config.get("bottom_buttons", [])
                
                response = json.dumps(bottom)
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(response.encode())
                print(f"[SERVER] Bottom buttons dikirim: {len(bottom)} tombol")
            except Exception as e:
                self._send_error(f"Gagal kirim bottom buttons: {e}")

        # MEDIA CONTROL
        elif self.path == "/media/playpause":
            self._send_keys("[char]179", "Media Play/Pause")
        elif self.path == "/media/next":
            self._send_keys("[char]176", "Media Next")
        elif self.path == "/media/prev":
            self._send_keys("[char]177", "Media Prev")

        # YOUTUBE
        elif self.path == "/youtube":
            try:
                chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
                subprocess.Popen([chrome_path, "https://www.youtube.com"])
                self._send_ok(b"YouTube dibuka")
            except Exception as e:
                self._send_error(f"Gagal buka YouTube: {e}")

        # GMAIL
        elif self.path == "/gmail":
            try:
                chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
                subprocess.Popen([chrome_path, "https://mail.google.com"])
                self._send_ok(b"Gmail dibuka")
            except Exception as e:
                self._send_error(f"Gagal buka Gmail: {e}")

        # GOOGLE
        elif self.path == "/google":
            try:
                chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
                subprocess.Popen([chrome_path, "https://www.google.com"])
                self._send_ok(b"Google dibuka")
            except Exception as e:
                self._send_error(f"Gagal buka Google: {e}")

        # DISCORD
        elif self.path == "/discord":
            try:
                os.startfile("discord://")
                self._send_ok(b"Discord dibuka")
            except Exception as e:
                self._send_error(f"Gagal buka Discord: {e}")

        # STEAM
        elif self.path == "/steam":
            try:
                os.startfile("steam://")
                self._send_ok(b"Steam dibuka")
            except Exception as e:
                self._send_error(f"Gagal buka Steam: {e}")

        # FOLDER SHORTCUTS
        elif self.path == "/downloads":
            try:
                subprocess.Popen(["explorer", os.path.expanduser("~\\Downloads")])
                self._send_ok(b"Downloads dibuka")
            except Exception as e:
                self._send_error(f"Gagal: {e}")

        elif self.path == "/documents":
            try:
                subprocess.Popen(["explorer", os.path.expanduser("~\\Documents")])
                self._send_ok(b"Documents dibuka")
            except Exception as e:
                self._send_error(f"Gagal: {e}")

        elif self.path == "/pictures":
            try:
                subprocess.Popen(["explorer", os.path.expanduser("~\\Pictures")])
                self._send_ok(b"Pictures dibuka")
            except Exception as e:
                self._send_error(f"Gagal: {e}")

        # VLC MEDIA
        elif self.path == "/vlc/playpause":
            self._send_keys("[char]179", "VLC Play/Pause")
        elif self.path == "/vlc/next":
            self._send_keys("[char]176", "VLC Next")
        elif self.path == "/vlc/prev":
            self._send_keys("[char]177", "VLC Prev")

        # SOUND
        elif self.path == "/sound/click":
            try:
                subprocess.Popen(
                    ["powershell", "-Command",
                     "[console]::beep(1000, 50)"],
                    shell=False
                )
                self._send_ok(b"Sound played")
            except Exception as e:
                self._send_error(f"Gagal: {e}")

        # TIDAK DITEMUKAN
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Endpoint tidak ditemukan")

    def _send_ok(self, message):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(message)

    def _send_error(self, message):
        print(f"[ERROR] {message}")
        self.send_response(500)
        self.end_headers()
        self.wfile.write(message.encode())

    def _send_keys(self, key, log_msg):
        try:
            subprocess.run(
                ["powershell", "-Command",
                 f"$obj = New-Object -ComObject WScript.Shell; "
                 f"$obj.SendKeys({key})"],
                capture_output=True
            )
            print(f"[SERVER] {log_msg}")
            self._send_ok(log_msg.encode())
        except Exception as e:
            self._send_error(f"Gagal: {e}")

# ==========================================================
# FUNGSI JALANKAN SERVER
# ==========================================================

def run_server():
    try:
        server = HTTPServer((HOST, PORT), Handler)
        print("=" * 60)
        print(f"[SERVER] Hafz Dashboard Server berjalan di port {PORT}")
        print(f"[SERVER] Config: {CONFIG_PATH}")
        print("=" * 60)
        server.serve_forever()
    except Exception as e:
        print(f"[SERVER] Error: {e}")

# ==========================================================
# GUI APLIKASI
# ==========================================================

class DashboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hafz Dashboard Settings")
        self.root.geometry("1000x650")
        self.root.configure(bg=BG_COLOR)
        
        self.config = load_config()
        self.current_profile = "default"
        
        self.setup_ui()
        self.refresh_profile_list()
        self.refresh_button_list()
        self.refresh_bottom_buttons()
    
    def setup_ui(self):
        # === HEADER ===
        header = tk.Frame(self.root, bg=CARD_COLOR, height=70)
        header.pack(fill="x", padx=10, pady=10)
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="🎯 HAFZ DASHBOARD SETTINGS",
            font=("Segoe UI", 18, "bold"),
            bg=CARD_COLOR,
            fg=TEXT_COLOR
        ).pack(side="left", padx=20)
        
        self.status_label = tk.Label(
            header,
            text="● Server: Online",
            font=("Segoe UI", 11, "bold"),
            bg=CARD_COLOR,
            fg=SUCCESS_COLOR
        )
        self.status_label.pack(side="right", padx=20)
        
        # === TABS ===
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Tab 1: Profiles
        self.profiles_tab = tk.Frame(self.notebook, bg=BG_COLOR)
        self.notebook.add(self.profiles_tab, text="📁 Profiles")
        self.setup_profiles_tab()
        
        # Tab 2: Bottom Buttons
        self.bottom_tab = tk.Frame(self.notebook, bg=BG_COLOR)
        self.notebook.add(self.bottom_tab, text="⬇️ Bottom Buttons")
        self.setup_bottom_tab()
        
        # Tab 3: About
        self.about_tab = tk.Frame(self.notebook, bg=BG_COLOR)
        self.notebook.add(self.about_tab, text="ℹ️ About")
        self.setup_about_tab()
    
    # ==================================================
    # TAB 1: PROFILES
    # ==================================================
    
    def setup_profiles_tab(self):
        main = tk.Frame(self.profiles_tab, bg=BG_COLOR)
        main.pack(fill="both", expand=True, padx=10, pady=10)
        
        # === LEFT: PROFILES ===
        left = tk.Frame(main, bg=CARD_COLOR, width=220)
        left.pack(side="left", fill="y", padx=(0, 10))
        left.pack_propagate(False)
        
        tk.Label(
            left,
            text="📁 Profiles",
            font=("Segoe UI", 12, "bold"),
            bg=CARD_COLOR,
            fg=TEXT_COLOR
        ).pack(pady=10)
        
        self.profile_listbox = tk.Listbox(
            left,
            bg=CARD_COLOR,
            fg=TEXT_COLOR,
            selectbackground=ACCENT_COLOR,
            font=("Segoe UI", 11),
            borderwidth=0,
            highlightthickness=0,
            activestyle="none"
        )
        self.profile_listbox.pack(fill="both", expand=True, padx=10, pady=5)
        self.profile_listbox.bind("<<ListboxSelect>>", self.on_profile_select)
        
        profile_btn_frame = tk.Frame(left, bg=CARD_COLOR)
        profile_btn_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Button(
            profile_btn_frame,
            text="➕ Profil",
            command=self.add_profile,
            bg=ACCENT_COLOR,
            fg="white",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            padx=10,
            pady=3
        ).pack(side="left", padx=2)
        
        tk.Button(
            profile_btn_frame,
            text="🗑️",
            command=self.delete_profile,
            bg=DANGER_COLOR,
            fg="white",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            padx=10,
            pady=3
        ).pack(side="left", padx=2)
        
        # === CENTER: BUTTONS ===
        center = tk.Frame(main, bg=CARD_COLOR)
        center.pack(side="left", fill="both", expand=True)
        
        tk.Label(
            center,
            text="🎛️ Buttons",
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
        self.button_tree.column("icon", width=120)
        self.button_tree.column("label", width=150)
        self.button_tree.column("endpoint", width=200)
        self.button_tree.column("color", width=100)
        self.button_tree.pack(fill="both", expand=True, padx=10, pady=5)
        self.button_tree.bind("<<TreeviewSelect>>", self.on_button_select)
        
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
            padx=15,
            pady=5
        ).pack(side="left", padx=3)
        
        tk.Button(
            btn_frame,
            text="✏️ Edit",
            command=self.edit_button,
            bg=WARNING_COLOR,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padx=15,
            pady=5
        ).pack(side="left", padx=3)
        
        tk.Button(
            btn_frame,
            text="🗑️ Hapus",
            command=self.delete_button,
            bg=DANGER_COLOR,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padx=15,
            pady=5
        ).pack(side="left", padx=3)
        
        tk.Button(
            btn_frame,
            text="🧪 Test",
            command=self.test_button,
            bg="#9C27B0",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padx=15,
            pady=5
        ).pack(side="left", padx=3)
        
        tk.Button(
            btn_frame,
            text="💾 Simpan",
            command=self.save_all,
            bg=SUCCESS_COLOR,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padx=15,
            pady=5
        ).pack(side="right", padx=3)
        
        # === RIGHT: PREVIEW ===
        right = tk.Frame(main, bg=CARD_COLOR, width=200)
        right.pack(side="right", fill="y", padx=(10, 0))
        right.pack_propagate(False)
        
        tk.Label(
            right,
            text="🖼️ Preview",
            font=("Segoe UI", 12, "bold"),
            bg=CARD_COLOR,
            fg=TEXT_COLOR
        ).pack(pady=10)
        
        self.preview_canvas = tk.Canvas(
            right,
            width=180,
            height=180,
            bg=BG_COLOR,
            highlightthickness=0
        )
        self.preview_canvas.pack(pady=10)
        
        self.preview_label = tk.Label(
            right,
            text="Pilih tombol\nuntuk preview",
            font=("Segoe UI", 10),
            bg=CARD_COLOR,
            fg=TEXT_SECONDARY
        )
        self.preview_label.pack(pady=10)
    
    # ==================================================
    # TAB 2: BOTTOM BUTTONS
    # ==================================================
    
    def setup_bottom_tab(self):
        main = tk.Frame(self.bottom_tab, bg=BG_COLOR)
        main.pack(fill="both", expand=True, padx=10, pady=10)
        
        tk.Label(
            main,
            text="⬇️ Tombol Bawah Dashboard",
            font=("Segoe UI", 14, "bold"),
            bg=BG_COLOR,
            fg=TEXT_COLOR
        ).pack(pady=10)
        
        tk.Label(
            main,
            text="Tombol ini akan muncul di BAWAH dashboard Android\n(di bawah Halaman 3 - PC Tools)",
            font=("Segoe UI", 10),
            bg=BG_COLOR,
            fg=TEXT_SECONDARY,
            justify="center"
        ).pack(pady=5)
        
        # Treeview
        columns = ("icon", "label", "endpoint", "color")
        self.bottom_tree = ttk.Treeview(
            main,
            columns=columns,
            show="headings",
            height=15
        )
        self.bottom_tree.heading("icon", text="Icon")
        self.bottom_tree.heading("label", text="Label")
        self.bottom_tree.heading("endpoint", text="Endpoint")
        self.bottom_tree.heading("color", text="Color")
        self.bottom_tree.column("icon", width=120)
        self.bottom_tree.column("label", width=150)
        self.bottom_tree.column("endpoint", width=200)
        self.bottom_tree.column("color", width=100)
        self.bottom_tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Buttons
        btn_frame = tk.Frame(main, bg=BG_COLOR)
        btn_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Button(
            btn_frame,
            text="➕ Tambah",
            command=self.add_bottom_button,
            bg=ACCENT_COLOR,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padx=15,
            pady=5
        ).pack(side="left", padx=3)
        
        tk.Button(
            btn_frame,
            text="✏️ Edit",
            command=self.edit_bottom_button,
            bg=WARNING_COLOR,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padx=15,
            pady=5
        ).pack(side="left", padx=3)
        
        tk.Button(
            btn_frame,
            text="🗑️ Hapus",
            command=self.delete_bottom_button,
            bg=DANGER_COLOR,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padx=15,
            pady=5
        ).pack(side="left", padx=3)
        
        tk.Button(
            btn_frame,
            text="💾 Simpan",
            command=self.save_all,
            bg=SUCCESS_COLOR,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padx=15,
            pady=5
        ).pack(side="right", padx=3)
    
    # ==================================================
    # TAB 3: ABOUT
    # ==================================================
    
    def setup_about_tab(self):
        main = tk.Frame(self.about_tab, bg=BG_COLOR)
        main.pack(fill="both", expand=True, padx=20, pady=20)
        
        tk.Label(
            main,
            text="🎯 Hafz Dashboard Settings",
            font=("Segoe UI", 20, "bold"),
            bg=BG_COLOR,
            fg=TEXT_COLOR
        ).pack(pady=20)
        
        tk.Label(
            main,
            text="Version 1.0.0",
            font=("Segoe UI", 12),
            bg=BG_COLOR,
            fg=TEXT_SECONDARY
        ).pack(pady=5)
        
        tk.Label(
            main,
            text="Software untuk mengatur tombol dashboard Android\nvia Wi-Fi.",
            font=("Segoe UI", 11),
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            justify="center"
        ).pack(pady=20)
        
        tk.Label(
            main,
            text="Fitur:\n"
                 "• Tambah/Edit/Hapus Tombol Dinamis (Profil)\n"
                 "• Tambah/Edit/Hapus Tombol Bawah\n"
                 "• Tambah/Hapus Profil\n"
                 "• Preview Icon\n"
                 "• Test Button\n"
                 "• Server HTTP terintegrasi",
            font=("Segoe UI", 10),
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            justify="left"
        ).pack(pady=20)
        
        tk.Label(
            main,
            text=f"Config: {CONFIG_PATH}",
            font=("Segoe UI", 9),
            bg=BG_COLOR,
            fg=TEXT_SECONDARY
        ).pack(pady=5)
    
    # ==================================================
    # FUNGSI REFRESH
    # ==================================================
    
    def refresh_profile_list(self):
        self.profile_listbox.delete(0, tk.END)
        profiles = list(self.config.get("profiles", {}).keys())
        for profile_name in profiles:
            self.profile_listbox.insert(tk.END, profile_name)
        
        if "default" in profiles:
            self.profile_listbox.selection_set(profiles.index("default"))
            self.current_profile = "default"
        elif profiles:
            self.profile_listbox.selection_set(0)
            self.current_profile = profiles[0]
    
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
    
    def refresh_bottom_buttons(self):
        for item in self.bottom_tree.get_children():
            self.bottom_tree.delete(item)
        
        buttons = self.config.get("bottom_buttons", [])
        
        for btn in buttons:
            self.bottom_tree.insert(
                "",
                "end",
                values=(
                    btn.get("icon", ""),
                    btn.get("label", ""),
                    btn.get("endpoint", ""),
                    btn.get("color", "")
                )
            )
    
    # ==================================================
    # EVENT HANDLERS
    # ==================================================
    
    def on_profile_select(self, event):
        selection = self.profile_listbox.curselection()
        if selection:
            self.current_profile = self.profile_listbox.get(selection[0])
            self.refresh_button_list()
    
    def on_button_select(self, event):
        selection = self.button_tree.selection()
        if selection:
            item = self.button_tree.item(selection[0])
            values = item["values"]
            self.show_preview(values[0], values[1])
    
    def show_preview(self, icon_name, label):
        self.preview_canvas.delete("all")
        
        icon_path_png = os.path.join(DRAWABLE_PATH, f"{icon_name}.png")
        
        if os.path.exists(icon_path_png):
            try:
                img = tk.PhotoImage(file=icon_path_png)
                w = img.width()
                h = img.height()
                
                if w > 160 or h > 160:
                    factor = max(w // 160, h // 160) + 1
                    img = img.subsample(factor, factor)
                
                self.preview_canvas.create_image(90, 90, image=img)
                self.preview_canvas.image = img
                self.preview_label.config(text=label, fg=TEXT_COLOR)
                return
            except Exception as e:
                print(f"Error load icon: {e}")
        
        self.preview_canvas.create_rectangle(20, 20, 160, 160, outline=TEXT_SECONDARY, width=2)
        self.preview_canvas.create_text(90, 90, text="❓", font=("Segoe UI", 40), fill=TEXT_SECONDARY)
        self.preview_label.config(text=f"{label}\n(icon tidak ada)", fg=WARNING_COLOR)
    
    # ==================================================
    # FUNGSI PROFIL
    # ==================================================
    
    def add_profile(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Tambah Profil")
        dialog.geometry("350x150")
        dialog.configure(bg=BG_COLOR)
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="Nama Profil:", bg=BG_COLOR, fg=TEXT_COLOR, font=("Segoe UI", 10)).pack(pady=10)
        
        entry = tk.Entry(dialog, font=("Segoe UI", 10), width=30)
        entry.pack(pady=5)
        entry.focus()
        
        def save():
            name = entry.get().strip().lower().replace(" ", "-")
            if not name:
                messagebox.showwarning("Peringatan", "Nama profil tidak boleh kosong!")
                return
            if name in self.config["profiles"]:
                messagebox.showwarning("Peringatan", f"Profil '{name}' sudah ada!")
                return
            
            self.config["profiles"][name] = []
            self.refresh_profile_list()
            dialog.destroy()
            messagebox.showinfo("Sukses", f"Profil '{name}' ditambahkan!")
        
        tk.Button(
            dialog,
            text="💾 Simpan",
            command=save,
            bg=SUCCESS_COLOR,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padx=20,
            pady=5
        ).pack(pady=10)
    
    def delete_profile(self):
        if self.current_profile == "default":
            messagebox.showwarning("Peringatan", "Profil 'default' tidak bisa dihapus!")
            return
        
        if messagebox.askyesno("Konfirmasi", f"Yakin mau hapus profil '{self.current_profile}'?"):
            del self.config["profiles"][self.current_profile]
            self.current_profile = "default"
            self.refresh_profile_list()
            self.refresh_button_list()
            messagebox.showinfo("Sukses", "Profil dihapus!")
    
    # ==================================================
    # FUNGSI TOMBOL DINAMIS
    # ==================================================
    
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
            messagebox.showinfo("Sukses", "Tombol diedit!")
    
    def delete_button(self):
        selection = self.button_tree.selection()
        if not selection:
            messagebox.showwarning("Peringatan", "Pilih tombol yang mau dihapus!")
            return
        
        if messagebox.askyesno("Konfirmasi", "Yakin mau hapus tombol ini?"):
            index = self.button_tree.index(selection[0])
            del self.config["profiles"][self.current_profile][index]
            self.refresh_button_list()
            messagebox.showinfo("Sukses", "Tombol dihapus!")
    
    def test_button(self):
        selection = self.button_tree.selection()
        if not selection:
            messagebox.showwarning("Peringatan", "Pilih tombol yang mau ditest!")
            return
        
        item = self.button_tree.item(selection[0])
        values = item["values"]
        endpoint = values[2]
        
        try:
            import urllib.request
            url = f"http://localhost:{PORT}{endpoint}"
            response = urllib.request.urlopen(url, timeout=5)
            result = response.read().decode()
            messagebox.showinfo("Test Berhasil", f"Endpoint: {endpoint}\n\nResponse: {result}")
        except Exception as e:
            messagebox.showerror("Test Gagal", f"Endpoint: {endpoint}\n\nError: {e}")
    
    # ==================================================
    # FUNGSI TOMBOL BAWAH
    # ==================================================
    
    def add_bottom_button(self):
        dialog = ButtonDialog(self.root, "Tambah Tombol Bawah")
        self.root.wait_window(dialog.dialog)
        
        if dialog.result:
            if "bottom_buttons" not in self.config:
                self.config["bottom_buttons"] = []
            
            self.config["bottom_buttons"].append(dialog.result)
            self.refresh_bottom_buttons()
            messagebox.showinfo("Sukses", "Tombol bawah ditambahkan! Klik 'Simpan' untuk menyimpan.")
    
    def edit_bottom_button(self):
        selection = self.bottom_tree.selection()
        if not selection:
            messagebox.showwarning("Peringatan", "Pilih tombol yang mau diedit!")
            return
        
        item = self.bottom_tree.item(selection[0])
        values = item["values"]
        
        old_button = {
            "icon": values[0],
            "label": values[1],
            "endpoint": values[2],
            "color": values[3]
        }
        
        dialog = ButtonDialog(self.root, "Edit Tombol Bawah", old_button)
        self.root.wait_window(dialog.dialog)
        
        if dialog.result:
            buttons = self.config["bottom_buttons"]
            index = self.bottom_tree.index(selection[0])
            buttons[index] = dialog.result
            self.refresh_bottom_buttons()
            messagebox.showinfo("Sukses", "Tombol bawah diedit!")
    
    def delete_bottom_button(self):
        selection = self.bottom_tree.selection()
        if not selection:
            messagebox.showwarning("Peringatan", "Pilih tombol yang mau dihapus!")
            return
        
        if messagebox.askyesno("Konfirmasi", "Yakin mau hapus tombol bawah ini?"):
            index = self.bottom_tree.index(selection[0])
            del self.config["bottom_buttons"][index]
            self.refresh_bottom_buttons()
            messagebox.showinfo("Sukses", "Tombol bawah dihapus!")
    
    def save_all(self):
        if save_config(self.config):
            messagebox.showinfo("Sukses", "Config berhasil disimpan!\n\nAndroid akan update otomatis dalam 30 detik.")
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
        self.dialog.geometry("420x400")
        self.dialog.configure(bg=BG_COLOR)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - 210
        y = (self.dialog.winfo_screenheight() // 2) - 200
        self.dialog.geometry(f"+{x}+{y}")
        
        form = tk.Frame(self.dialog, bg=BG_COLOR)
        form.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Icon
        tk.Label(form, text="Icon:", bg=BG_COLOR, fg=TEXT_COLOR, font=("Segoe UI", 11)).grid(row=0, column=0, sticky="w", pady=8)
        self.icon_entry = tk.Entry(form, font=("Segoe UI", 11), width=30)
        self.icon_entry.grid(row=0, column=1, pady=8, padx=10)
        
        tk.Label(form, text="(nama file icon tanpa .png)", bg=BG_COLOR, fg=TEXT_SECONDARY, font=("Segoe UI", 8)).grid(row=1, column=1, sticky="w", padx=10)
        
        # Label
        tk.Label(form, text="Label:", bg=BG_COLOR, fg=TEXT_COLOR, font=("Segoe UI", 11)).grid(row=2, column=0, sticky="w", pady=8)
        self.label_entry = tk.Entry(form, font=("Segoe UI", 11), width=30)
        self.label_entry.grid(row=2, column=1, pady=8, padx=10)
        
        # Endpoint
        tk.Label(form, text="Endpoint:", bg=BG_COLOR, fg=TEXT_COLOR, font=("Segoe UI", 11)).grid(row=3, column=0, sticky="w", pady=8)
        self.endpoint_entry = tk.Entry(form, font=("Segoe UI", 11), width=30)
        self.endpoint_entry.grid(row=3, column=1, pady=8, padx=10)
        
        tk.Label(form, text="(contoh: /discord)", bg=BG_COLOR, fg=TEXT_SECONDARY, font=("Segoe UI", 8)).grid(row=4, column=1, sticky="w", padx=10)
        
        # Color
        tk.Label(form, text="Color:", bg=BG_COLOR, fg=TEXT_COLOR, font=("Segoe UI", 11)).grid(row=5, column=0, sticky="w", pady=8)
        self.color_var = tk.StringVar(value="blue")
        color_combo = ttk.Combobox(
            form,
            textvariable=self.color_var,
            values=["green", "blue", "purple", "orange", "red", "cyan"],
            state="readonly",
            font=("Segoe UI", 11),
            width=28
        )
        color_combo.grid(row=5, column=1, pady=8, padx=10)
        
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
            bg=SUCCESS_COLOR,
            fg="white",
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            padx=25,
            pady=8
        ).pack(side="right", padx=5)
        
        tk.Button(
            btn_frame,
            text="❌ Batal",
            command=self.dialog.destroy,
            bg=DANGER_COLOR,
            fg="white",
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            padx=25,
            pady=8
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
    print("=" * 60)
    print("  🎯 HAFZ DASHBOARD SETTINGS")
    print("=" * 60)
    
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    print("[MAIN] Server berjalan di background")
    print("[MAIN] Membuka GUI...")
    
    root = tk.Tk()
    app = DashboardApp(root)
    root.mainloop()
    
    print("[MAIN] Dihentikan")