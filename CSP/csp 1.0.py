# CSP — Create a Server on this PC
# Версия 1.0
# Создатель: Саша

import tkinter as tk
from tkinter import filedialog, messagebox
import http.server
import socketserver
import threading
import os
import socket
import webbrowser
import urllib.request

# ============ НАСТРОЙКИ ============
PORT = 8080
server = None
server_thread = None
is_running = False
site_folder = ""

# ============ IP ============
def get_local_ip():
    """Локальный IP-адрес"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def get_public_ip():
    """Публичный IP-адрес"""
    try:
        return urllib.request.urlopen("https://api.ipify.org").read().decode()
    except:
        return "не удалось получить"

# ============ СЕРВЕР ============
class CSPHandler(http.server.SimpleHTTPRequestHandler):
    """Обработчик запросов с логами"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=site_folder, **kwargs)
    
    def log_message(self, format, *args):
        """Логи в текстовое поле"""
        log_text.config(state=tk.NORMAL)
        log_text.insert(tk.END, f"[{self.log_date_time_string()}] {format % args}\n")
        log_text.see(tk.END)
        log_text.config(state=tk.DISABLED)

def start_server():
    """Запускает сервер"""
    global server, server_thread, is_running, site_folder
    
    if not site_folder:
        messagebox.showerror("CSP", "Выбери папку с сайтом!")
        return
    
    if not os.path.exists(site_folder):
        messagebox.showerror("CSP", "Папка не найдена!")
        return
    
    try:
        server = socketserver.TCPServer(("", PORT), CSPHandler)
        server_thread = threading.Thread(target=server.serve_forever, daemon=True)
        server_thread.start()
        
        is_running = True
        status_label.config(text=f"🟢 Сервер работает на порту {PORT}", fg="#32CD32")
        start_btn.config(state=tk.DISABLED)
        stop_btn.config(state=tk.NORMAL)
        
        local_ip = get_local_ip()
        public_ip = get_public_ip()
        
        log_text.config(state=tk.NORMAL)
        log_text.insert(tk.END, "=" * 50 + "\n")
        log_text.insert(tk.END, "🟢 CSP — СЕРВЕР ЗАПУЩЕН!\n")
        log_text.insert(tk.END, "=" * 50 + "\n")
        log_text.insert(tk.END, f"📁 Папка: {site_folder}\n")
        log_text.insert(tk.END, f"🌐 Локально: http://localhost:{PORT}\n")
        log_text.insert(tk.END, f"🏠 Локальная сеть: http://{local_ip}:{PORT}\n")
        log_text.insert(tk.END, f"🌍 Публично: http://{public_ip}:{PORT}\n")
        log_text.insert(tk.END, "=" * 50 + "\n\n")
        log_text.see(tk.END)
        log_text.config(state=tk.DISABLED)
        
        webbrowser.open(f"http://localhost:{PORT}")
        
    except OSError as e:
        if "Address already in use" in str(e):
            messagebox.showerror("CSP", f"Порт {PORT} занят!\nПопробуй другой порт.")
        else:
            messagebox.showerror("CSP", f"Ошибка:\n{e}")

def stop_server():
    """Останавливает сервер"""
    global server, is_running
    
    if server:
        server.shutdown()
        server.server_close()
        server = None
    
    is_running = False
    status_label.config(text="🔴 Сервер остановлен", fg="#C42B1C")
    start_btn.config(state=tk.NORMAL)
    stop_btn.config(state=tk.DISABLED)
    
    log_text.config(state=tk.NORMAL)
    log_text.insert(tk.END, "\n🔴 СЕРВЕР ОСТАНОВЛЕН\n\n")
    log_text.see(tk.END)
    log_text.config(state=tk.DISABLED)

def choose_folder():
    """Выбор папки с сайтом"""
    global site_folder
    folder = filedialog.askdirectory(title="Выбери папку с сайтом")
    if folder:
        site_folder = folder
        folder_label.config(text=f"📁 {folder}")
        
        if os.path.exists(os.path.join(folder, "index.html")):
            log_text.config(state=tk.NORMAL)
            log_text.insert(tk.END, f"✅ Найден index.html в {folder}\n")
            log_text.see(tk.END)
            log_text.config(state=tk.DISABLED)
        else:
            log_text.config(state=tk.NORMAL)
            log_text.insert(tk.END, f"⚠️ index.html не найден в {folder}\n")
            log_text.see(tk.END)
            log_text.config(state=tk.DISABLED)

def open_in_browser():
    """Открыть в браузере"""
    if is_running:
        webbrowser.open(f"http://localhost:{PORT}")
    else:
        messagebox.showwarning("CSP", "Сервер не запущен!")

# ============ ИНТЕРФЕЙС ============
root = tk.Tk()
root.title("CSP — Create a Server on this PC")
root.geometry("700x650")
root.configure(bg="#0a0a1a")

# Заголовок
tk.Label(root, text="🖥 CSP", font=("Arial", 32, "bold"),
         bg="#0a0a1a", fg="#FFFFFF").pack(pady=15)
tk.Label(root, text="CREATE A SERVER ON THIS PC", font=("Arial", 12, "bold"),
         bg="#0a0a1a", fg="#00BFFF").pack()
tk.Label(root, text="Твой ПК — сервер для сайта", font=("Arial", 11),
         bg="#0a0a1a", fg="#888888").pack(pady=5)

# Папка
frame1 = tk.Frame(root, bg="#0a0a1a")
frame1.pack(pady=15, padx=20, fill="x")

tk.Button(frame1, text="📁 Выбрать папку с сайтом", command=choose_folder,
          bg="#0066CC", fg="white", font=("Arial", 12, "bold"),
          padx=20, pady=10).pack(side="left")

folder_label = tk.Label(frame1, text="📁 Папка не выбрана", bg="#0a0a1a",
                        fg="#FFD700", font=("Arial", 10), wraplength=400,
                        justify="left")
folder_label.pack(side="left", padx=10)

# Кнопки
frame2 = tk.Frame(root, bg="#0a0a1a")
frame2.pack(pady=10)

start_btn = tk.Button(frame2, text="▶ Запустить сервер", command=start_server,
                      bg="#32CD32", fg="white", font=("Arial", 14, "bold"),
                      padx=30, pady=15)
start_btn.pack(side="left", padx=10)

stop_btn = tk.Button(frame2, text="⏹ Остановить", command=stop_server,
                     bg="#C42B1C", fg="white", font=("Arial", 14, "bold"),
                     padx=30, pady=15, state=tk.DISABLED)
stop_btn.pack(side="left", padx=10)

# Открыть в браузере
tk.Button(root, text="🌐 Открыть в браузере", command=open_in_browser,
          bg="#0066CC", fg="white", font=("Arial", 11),
          padx=20, pady=8).pack(pady=10)

# Статус
status_label = tk.Label(root, text="🔴 Сервер остановлен", bg="#0a0a1a",
                        fg="#C42B1C", font=("Arial", 14, "bold"))
status_label.pack(pady=10)

# Логи
tk.Label(root, text="📊 Логи сервера:", bg="#0a0a1a", fg="white",
         font=("Arial", 11, "bold")).pack(anchor="w", padx=20)

log_text = tk.Text(root, bg="#000000", fg="#00FF00", font=("Courier", 9),
                   height=12, wrap="word")
log_text.pack(fill="both", expand=True, padx=20, pady=10)
log_text.config(state=tk.DISABLED)

# Подвал
tk.Label(root, text="CSP v1.0 • Create a Server on this PC • Создатель: Саша",
         bg="#0a0a1a", fg="#666666", font=("Arial", 9)).pack(pady=5)

# ============ ЗАПУСК ============
root.mainloop()