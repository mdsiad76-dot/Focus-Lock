"""
Focus Lock - keeps you inside your class app until the timer ends.

How it works
  * You pick your class app (e.g. ACS) and any other apps allowed (e.g. WhatsApp).
  * Start the timer. If any other window comes to the front, it is minimized
    and your class app is brought back immediately.
  * If the class app gets closed, it is relaunched.
  * You can't close this timer window until time is up.
    (Emergency stop exists, but you must type a long random text.)

Run:  python focus_lock.py        (Windows only, Python 3.8+)
"""
import ctypes
import json
import os
import random
import string
import subprocess
import time
import tkinter as tk
from ctypes import wintypes
from tkinter import ttk, messagebox

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

kernel32.OpenProcess.restype = wintypes.HANDLE
kernel32.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
kernel32.QueryFullProcessImageNameW.argtypes = [
    wintypes.HANDLE, wintypes.DWORD, wintypes.LPWSTR, ctypes.POINTER(wintypes.DWORD)]
user32.GetForegroundWindow.restype = wintypes.HWND
user32.SetForegroundWindow.argtypes = [wintypes.HWND]
user32.ShowWindow.argtypes = [wintypes.HWND, ctypes.c_int]
user32.IsIconic.argtypes = [wintypes.HWND]

SW_MINIMIZE, SW_RESTORE = 6, 9
SETTINGS_FILE = os.path.join(os.path.expanduser("~"), ".focus_lock.json")

# Windows shell pieces (taskbar, desktop, Alt+Tab, Start menu). We don't minimize
# these, we just pull focus back to the class app.
SHELL_CLASSES = {
    "Shell_TrayWnd", "Shell_SecondaryTrayWnd", "Progman", "WorkerW",
    "TaskListThumbnailWnd", "MultitaskingViewFrame", "XamlExplorerHostIslandWindow",
    "ForegroundStaging", "Windows.UI.Core.CoreWindow", "TaskSwitcherWnd",
}


# ---------- Windows helpers ----------
def win_pid(hwnd):
    pid = wintypes.DWORD()
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    return pid.value


def win_text(hwnd):
    n = user32.GetWindowTextLengthW(hwnd)
    buf = ctypes.create_unicode_buffer(n + 1)
    user32.GetWindowTextW(hwnd, buf, n + 1)
    return buf.value


def win_class(hwnd):
    buf = ctypes.create_unicode_buffer(256)
    user32.GetClassNameW(hwnd, buf, 256)
    return buf.value


def proc_path(pid):
    h = kernel32.OpenProcess(0x1000, False, pid)  # QUERY_LIMITED_INFORMATION
    if not h:
        return ""
    try:
        buf = ctypes.create_unicode_buffer(1024)
        size = wintypes.DWORD(1024)
        if kernel32.QueryFullProcessImageNameW(h, 0, buf, ctypes.byref(size)):
            return buf.value
    finally:
        kernel32.CloseHandle(h)
    return ""


def list_windows():
    """Visible top-level windows with a title -> list of dicts."""
    out = []
    PROC = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)

    def cb(hwnd, _):
        if user32.IsWindowVisible(hwnd) and user32.GetWindowTextLengthW(hwnd) > 0:
            path = proc_path(win_pid(hwnd))
            if path:
                out.append({"hwnd": hwnd, "path": path,
                            "exe": os.path.basename(path).lower(),
                            "title": win_text(hwnd)})
        return True

    user32.EnumWindows(PROC(cb), 0)
    return out


def force_foreground(hwnd):
    if user32.IsIconic(hwnd):
        user32.ShowWindow(hwnd, SW_RESTORE)
    # Tapping ALT lets SetForegroundWindow work from a background process.
    user32.keybd_event(0x12, 0, 0, 0)
    user32.keybd_event(0x12, 0, 2, 0)
    user32.SetForegroundWindow(hwnd)


def split_keywords(text):
    return [k.strip().lower() for k in text.split(",") if k.strip()]


# ---------- App ----------
class FocusLock(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Focus Lock")
        self.resizable(False, False)
        self.running = False
        self.end = 0
        self.last_relaunch_check = 0
        self.cfg = self.load_cfg()
        self.exes = []
        self.paths = {}
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.build_setup()

    # settings
    def load_cfg(self):
        try:
            with open(SETTINGS_FILE, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

    def save_cfg(self):
        try:
            with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
                json.dump(self.cfg, f)
        except Exception:
            pass

    # ---------- setup screen ----------
    def build_setup(self):
        for w in self.winfo_children():
            w.destroy()
        self.attributes("-topmost", False)
        f = ttk.Frame(self, padding=14)
        f.grid()

        ttk.Label(f, text="1. Your class app (stays in front):").grid(sticky="w")
        self.main_var = tk.StringVar(value=self.cfg.get("main", ""))
        self.main_cb = ttk.Combobox(f, textvariable=self.main_var, state="readonly", width=40)
        self.main_cb.grid(sticky="we")

        ttk.Label(f, text="2. Other apps allowed (Ctrl+click for many):").grid(sticky="w", pady=(10, 0))
        self.lb = tk.Listbox(f, selectmode=tk.MULTIPLE, height=9, width=42, exportselection=False)
        self.lb.grid(sticky="we")

        ttk.Button(f, text="Refresh app list", command=self.refresh_apps).grid(sticky="w", pady=4)

        ttk.Label(f, text="Always block windows with these words in the title\n(useful if class runs in a browser):").grid(sticky="w", pady=(6, 0))
        self.block_var = tk.StringVar(value=self.cfg.get("block", "instagram, facebook, youtube, tiktok"))
        ttk.Entry(f, textvariable=self.block_var, width=45).grid(sticky="we")

        ttk.Label(f, text="Also allow windows with these words in the title\n(e.g. whatsapp for the Store version):").grid(sticky="w", pady=(6, 0))
        self.allow_var = tk.StringVar(value=self.cfg.get("allow_words", "whatsapp"))
        ttk.Entry(f, textvariable=self.allow_var, width=45).grid(sticky="we")

        row = ttk.Frame(f)
        row.grid(sticky="w", pady=(10, 0))
        ttk.Label(row, text="Minutes:").pack(side="left")
        self.min_var = tk.IntVar(value=self.cfg.get("minutes", 45))
        ttk.Spinbox(row, from_=1, to=600, textvariable=self.min_var, width=6).pack(side="left", padx=6)
        ttk.Button(row, text="START LOCK", command=self.start).pack(side="left", padx=12)

        self.refresh_apps()

    def refresh_apps(self):
        wins = list_windows()
        me = os.path.basename(os.sys.executable).lower()
        self.paths = {}
        for w in wins:
            if w["exe"] in (me, "explorer.exe", "textinputhost.exe"):
                continue
            self.paths.setdefault(w["exe"], w["path"])
        self.exes = sorted(self.paths)
        self.main_cb["values"] = self.exes
        self.lb.delete(0, tk.END)
        saved = set(self.cfg.get("allowed", []))
        for i, e in enumerate(self.exes):
            self.lb.insert(tk.END, e)
            if e in saved:
                self.lb.selection_set(i)

    # ---------- session ----------
    def start(self):
        main = self.main_var.get()
        if not main:
            messagebox.showwarning("Focus Lock", "Open your class app first, click 'Refresh app list', then choose it.")
            return
        minutes = int(self.min_var.get())
        self.allowed = {self.exes[i] for i in self.lb.curselection()} | {main}
        self.block_words = split_keywords(self.block_var.get())
        self.allow_words = split_keywords(self.allow_var.get())
        self.main_exe = main
        self.main_path = self.paths.get(main, "")
        self.cfg.update(main=main, allowed=sorted(self.allowed), minutes=minutes,
                        block=self.block_var.get(), allow_words=self.allow_var.get())
        self.save_cfg()

        self.end = time.time() + minutes * 60
        self.running = True
        self.build_session()
        force_foreground_main = self.find_main_window()
        if force_foreground_main:
            force_foreground(force_foreground_main)
        self.tick()

    def build_session(self):
        for w in self.winfo_children():
            w.destroy()
        self.attributes("-topmost", True)
        f = ttk.Frame(self, padding=12)
        f.grid()
        ttk.Label(f, text="LOCKED - finish your class", font=("Segoe UI", 10, "bold")).grid()
        self.time_lbl = ttk.Label(f, text="", font=("Consolas", 30, "bold"))
        self.time_lbl.grid(pady=4)
        ttk.Button(f, text="Emergency stop", command=self.emergency).grid()
        # park the small timer window at the top-right corner
        self.update_idletasks()
        x = self.winfo_screenwidth() - self.winfo_reqwidth() - 20
        self.geometry(f"+{x}+20")

    def find_main_window(self):
        for w in list_windows():
            if w["exe"] == self.main_exe:
                return w["hwnd"]
        return None

    def tick(self):
        if not self.running:
            return
        remaining = int(self.end - time.time())
        if remaining <= 0:
            self.finish()
            return
        h, rem = divmod(remaining, 3600)
        m, s = divmod(rem, 60)
        self.time_lbl.config(text=f"{h:02d}:{m:02d}:{s:02d}")
        try:
            self.enforce()
        except Exception:
            pass
        self.after(300, self.tick)

    def is_allowed(self, exe, title):
        t = title.lower()
        if any(k in t for k in self.block_words):
            return False
        return exe in self.allowed or any(k in t for k in self.allow_words)

    def enforce(self):
        # relaunch class app if it was closed
        now = time.time()
        if now - self.last_relaunch_check > 3:
            self.last_relaunch_check = now
            if not self.find_main_window() and self.main_path and \
                    self.main_exe != "applicationframehost.exe":
                try:
                    subprocess.Popen([self.main_path])
                except Exception:
                    pass

        fg = user32.GetForegroundWindow()
        if not fg or win_pid(fg) == os.getpid():
            return
        cls = win_class(fg)
        exe = os.path.basename(proc_path(win_pid(fg))).lower()
        title = win_text(fg)

        if cls in SHELL_CLASSES:
            target = self.find_main_window()
            if target:
                force_foreground(target)
            return
        if self.is_allowed(exe, title):
            return
        user32.ShowWindow(fg, SW_MINIMIZE)
        target = self.find_main_window()
        if target:
            force_foreground(target)

    def finish(self):
        self.running = False
        self.attributes("-topmost", False)
        messagebox.showinfo("Focus Lock", "Time is up - great job! You're free now.")
        self.build_setup()

    def emergency(self):
        text = "".join(random.choices(string.ascii_lowercase + string.digits, k=40))
        win = tk.Toplevel(self)
        win.title("Emergency stop")
        win.attributes("-topmost", True)
        ttk.Label(win, text="Type this text exactly to stop early:", padding=8).pack()
        ttk.Label(win, text=text, font=("Consolas", 12, "bold"), padding=4).pack()
        var = tk.StringVar()
        e = ttk.Entry(win, textvariable=var, width=46)
        e.pack(padx=10, pady=6)
        e.focus_set()

        def check():
            if var.get().strip() == text:
                self.running = False
                win.destroy()
                self.attributes("-topmost", False)
                self.build_setup()
            else:
                messagebox.showwarning("Focus Lock", "Doesn't match. Keep studying!", parent=win)

        ttk.Button(win, text="Stop lock", command=check).pack(pady=(0, 10))

    def on_close(self):
        if self.running:
            self.bell()  # can't close during a session
        else:
            self.destroy()


if __name__ == "__main__":
    FocusLock().mainloop()
