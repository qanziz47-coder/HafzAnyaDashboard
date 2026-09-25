from http.server import BaseHTTPRequestHandler, HTTPServer
import subprocess
import os
import json


# ==========================================================
# KONFIGURASI
# ==========================================================

HOST = "0.0.0.0"
PORT = 5000

# Path ke config.json (satu folder dengan server.py)
CONFIG_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "config.json"
)


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
        
        app_name = result.stdout.strip()
        print(f"DEBUG: Active app = '{app_name}'")
        return app_name
        
    except Exception as e:
        print(f"DEBUG: Error deteksi app: {e}")
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
    """Mapping nama aplikasi ke profil (case-insensitive)"""
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
# FUNGSI BACA/SIMPAN CONFIG
# ==========================================================

def load_config():
    """Baca config.json"""
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error baca config: {e}")
        return {"profiles": {}}


# ==========================================================
# HANDLER
# ==========================================================

class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        print(f"Menerima request: {self.path}")

        # SPOTIFY
        if self.path == "/spotify":
            try:
                os.startfile("spotify:")
                print("Spotify dibuka")
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"Spotify dibuka")
            except Exception as e:
                print(f"Gagal buka Spotify: {e}")
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b"Gagal buka Spotify")

        # CHROME
        elif self.path == "/chrome":
            try:
                chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
                subprocess.Popen([chrome_path])
                print("Chrome dibuka")
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"Chrome dibuka")
            except Exception as e:
                print(f"Gagal buka Chrome: {e}")
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b"Gagal buka Chrome")

        # FILE EXPLORER
        elif self.path == "/file":
            try:
                subprocess.Popen(["explorer", "C:\\"])
                print("File Explorer dibuka")
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"File Explorer dibuka")
            except Exception as e:
                print(f"Gagal buka File Explorer: {e}")
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b"Gagal buka File Explorer")

        # WHATSAPP
        elif self.path == "/whatsapp":
            try:
                os.startfile("whatsapp://")
                print("WhatsApp dibuka")
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"WhatsApp dibuka")
            except Exception as e:
                print(f"Gagal buka WhatsApp: {e}")
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b"Gagal buka WhatsApp")

        # SHUTDOWN
        elif self.path == "/shutdown":
            try:
                subprocess.Popen(["shutdown", "/s", "/t", "10"])
                print("PC akan shutdown dalam 10 detik")
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"Shutdown dalam 10 detik")
            except Exception as e:
                print(f"Gagal shutdown: {e}")
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b"Gagal shutdown")

        # RESTART
        elif self.path == "/restart":
            try:
                subprocess.Popen(["shutdown", "/r", "/t", "10"])
                print("PC akan restart dalam 10 detik")
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"Restart dalam 10 detik")
            except Exception as e:
                print(f"Gagal restart: {e}")
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b"Gagal restart")

        # LOCK
        elif self.path == "/lock":
            try:
                subprocess.Popen(["rundll32.exe", "user32.dll,LockWorkStation"])
                print("PC dikunci")
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"PC dikunci")
            except Exception as e:
                print(f"Gagal lock: {e}")
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b"Gagal lock")

        # CMD
        elif self.path == "/cmd":
            try:
                subprocess.Popen(
                    "start cmd.exe",
                    shell=True,
                    creationflags=subprocess.CREATE_NEW_CONSOLE
                )
                print("CMD dibuka")
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"CMD dibuka")
            except Exception as e:
                print(f"Gagal buka CMD: {e}")
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b"Gagal buka CMD")

        # CALCULATOR
        elif self.path == "/calc":
            try:
                subprocess.Popen("start calc.exe", shell=True)
                print("Calculator dibuka")
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"Calculator dibuka")
            except Exception as e:
                print(f"Gagal buka Calculator: {e}")
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b"Gagal buka Calculator")

        # TASK MANAGER
        elif self.path == "/taskmgr":
            try:
                subprocess.Popen("start taskmgr.exe", shell=True)
                print("Task Manager dibuka")
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"Task Manager dibuka")
            except Exception as e:
                print(f"Gagal buka Task Manager: {e}")
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b"Gagal buka Task Manager")

        # SLEEP
        elif self.path == "/sleep":
            try:
                subprocess.Popen(["rundll32.exe", "powrprof.dll,SetSuspendState", "0,1,0"])
                print("PC sleep")
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"PC sleep")
            except Exception as e:
                print(f"Gagal sleep: {e}")
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b"Gagal sleep")

        # SETTINGS
        elif self.path == "/settings":
            try:
                subprocess.Popen(["start", "ms-settings:"], shell=True)
                print("Settings dibuka")
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"Settings dibuka")
            except Exception as e:
                print(f"Gagal buka Settings: {e}")
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b"Gagal buka Settings")

        # STATS (CPU & RAM)
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
                print(f"Stats: CPU={cpu}% RAM={ram}%")

            except Exception as e:
                print(f"Gagal baca stats: {e}")
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b'{"error": "Gagal baca stats"}')

        # UPTIME PC
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
                    result2 = subprocess.run(
                        ["powershell", "-Command",
                         "[math]::Floor((New-TimeSpan -Start (Get-CimInstance Win32_OperatingSystem).LastBootUpTime).TotalMinutes)"],
                        capture_output=True, text=True, timeout=10
                    )
                    total_min = int(result2.stdout.strip() or 0)
                    hours = total_min // 60
                    minutes = total_min % 60
                    uptime_str = f"{hours}:{minutes}"
                
                print(f"Uptime: {uptime_str}")
                
                response = json.dumps({"uptime": uptime_str})
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(response.encode())

            except Exception as e:
                print(f"Gagal baca uptime: {e}")
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
                print(f"Active app: {app_name} -> profile: {profile}")
            except Exception as e:
                print(f"Gagal deteksi app: {e}")
                response = json.dumps({"app": "", "profile": "default"})
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(response.encode())

        # ==================================================
        # PROFILES (BACA DARI config.json)
        # ==================================================
        elif self.path == "/profiles":
            try:
                config = load_config()
                profiles = config.get("profiles", {})
                
                response = json.dumps(profiles)
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(response.encode())
                print(f"Profiles dikirim dari config.json ({len(profiles)} profil)")
            except Exception as e:
                print(f"Gagal kirim profiles: {e}")
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b'{"error": "Gagal"}')

        # MEDIA CONTROL
        elif self.path == "/media/playpause":
            try:
                subprocess.run(
                    ["powershell", "-Command",
                     "$obj = New-Object -ComObject WScript.Shell; "
                     "$obj.SendKeys([char]179)"],
                    capture_output=True
                )
                print("Media Play/Pause")
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"Play/Pause")
            except Exception as e:
                print(f"Gagal media: {e}")
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b"Gagal")

        elif self.path == "/media/next":
            try:
                subprocess.run(
                    ["powershell", "-Command",
                     "$obj = New-Object -ComObject WScript.Shell; "
                     "$obj.SendKeys([char]176)"],
                    capture_output=True
                )
                print("Media Next")
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"Next")
            except Exception as e:
                print(f"Gagal media: {e}")
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b"Gagal")

        elif self.path == "/media/prev":
            try:
                subprocess.run(
                    ["powershell", "-Command",
                     "$obj = New-Object -ComObject WScript.Shell; "
                     "$obj.SendKeys([char]177)"],
                    capture_output=True
                )
                print("Media Prev")
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"Prev")
            except Exception as e:
                print(f"Gagal media: {e}")
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b"Gagal")

        # YOUTUBE
        elif self.path == "/youtube":
            try:
                chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
                subprocess.Popen([chrome_path, "https://www.youtube.com"])
                print("YouTube dibuka")
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"YouTube dibuka")
            except Exception as e:
                print(f"Gagal buka YouTube: {e}")
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b"Gagal buka YouTube")

        # GMAIL
        elif self.path == "/gmail":
            try:
                chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
                subprocess.Popen([chrome_path, "https://mail.google.com"])
                print("Gmail dibuka")
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"Gmail dibuka")
            except Exception as e:
                print(f"Gagal buka Gmail: {e}")
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b"Gagal buka Gmail")

        # GOOGLE
        elif self.path == "/google":
            try:
                chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
                subprocess.Popen([chrome_path, "https://www.google.com"])
                print("Google dibuka")
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"Google dibuka")
            except Exception as e:
                print(f"Gagal buka Google: {e}")
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b"Gagal buka Google")

        # DISCORD
        elif self.path == "/discord":
            try:
                os.startfile("discord://")
                print("Discord dibuka")
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"Discord dibuka")
            except Exception as e:
                print(f"Gagal buka Discord: {e}")
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b"Gagal buka Discord")

        # STEAM
        elif self.path == "/steam":
            try:
                os.startfile("steam://")
                print("Steam dibuka")
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"Steam dibuka")
            except Exception as e:
                print(f"Gagal buka Steam: {e}")
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b"Gagal buka Steam")

        # FOLDER SHORTCUTS
        elif self.path == "/downloads":
            try:
                subprocess.Popen(["explorer", os.path.expanduser("~\\Downloads")])
                print("Downloads dibuka")
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"Downloads dibuka")
            except Exception as e:
                print(f"Gagal: {e}")
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b"Gagal")

        elif self.path == "/documents":
            try:
                subprocess.Popen(["explorer", os.path.expanduser("~\\Documents")])
                print("Documents dibuka")
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"Documents dibuka")
            except Exception as e:
                print(f"Gagal: {e}")
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b"Gagal")

        elif self.path == "/pictures":
            try:
                subprocess.Popen(["explorer", os.path.expanduser("~\\Pictures")])
                print("Pictures dibuka")
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"Pictures dibuka")
            except Exception as e:
                print(f"Gagal: {e}")
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b"Gagal")

        # VLC MEDIA CONTROL
        elif self.path == "/vlc/playpause":
            try:
                subprocess.run(
                    ["powershell", "-Command",
                     "$obj = New-Object -ComObject WScript.Shell; "
                     "$obj.SendKeys([char]179)"],
                    capture_output=True
                )
                print("VLC Play/Pause")
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"VLC Play/Pause")
            except Exception as e:
                print(f"Gagal: {e}")
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b"Gagal")

        elif self.path == "/vlc/next":
            try:
                subprocess.run(
                    ["powershell", "-Command",
                     "$obj = New-Object -ComObject WScript.Shell; "
                     "$obj.SendKeys([char]176)"],
                    capture_output=True
                )
                print("VLC Next")
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"VLC Next")
            except Exception as e:
                print(f"Gagal: {e}")
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b"Gagal")

        elif self.path == "/vlc/prev":
            try:
                subprocess.run(
                    ["powershell", "-Command",
                     "$obj = New-Object -ComObject WScript.Shell; "
                     "$obj.SendKeys([char]177)"],
                    capture_output=True
                )
                print("VLC Prev")
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"VLC Prev")
            except Exception as e:
                print(f"Gagal: {e}")
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b"Gagal")

        # SOUND EFFECT
        elif self.path == "/sound/click":
            try:
                subprocess.Popen(
                    ["powershell", "-Command",
                     "[console]::beep(1000, 50)"],
                    shell=False
                )
                print("Sound: click")
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"Sound played")
            except Exception as e:
                print(f"Gagal putar suara: {e}")
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b"Gagal")

        # TIDAK DITEMUKAN
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Endpoint tidak ditemukan")


# ==========================================================
# MENJALANKAN SERVER
# ==========================================================

if __name__ == "__main__":
    server = HTTPServer((HOST, PORT), Handler)
    print("=" * 50)
    print(f"Hafz Dashboard Server berjalan di port {PORT}")
    print("=" * 50)
    print(f"Config     : {CONFIG_PATH}")
    print(f"Spotify    : http://192.168.1.11:{PORT}/spotify")
    print(f"Chrome     : http://192.168.1.11:{PORT}/chrome")
    print(f"File       : http://192.168.1.11:{PORT}/file")
    print(f"WhatsApp   : http://192.168.1.11:{PORT}/whatsapp")
    print(f"CMD        : http://192.168.1.11:{PORT}/cmd")
    print(f"Calculator : http://192.168.1.11:{PORT}/calc")
    print(f"TaskMgr    : http://192.168.1.11:{PORT}/taskmgr")
    print(f"Sleep      : http://192.168.1.11:{PORT}/sleep")
    print(f"Settings   : http://192.168.1.11:{PORT}/settings")
    print(f"Stats      : http://192.168.1.11:{PORT}/stats")
    print(f"Uptime     : http://192.168.1.11:{PORT}/uptime")
    print(f"Active App : http://192.168.1.11:{PORT}/active-app")
    print(f"Profiles   : http://192.168.1.11:{PORT}/profiles")
    print("=" * 50)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer dihentikan.")
        server.server_close()