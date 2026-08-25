import sys
import mss
import cv2
import numpy as np
import time
import threading
import ctypes
import random
import tkinter as tk
from tkinter import scrolledtext, ttk
from pynput import keyboard
import os

# ==========================================
# 1. DYNAMIC PATH RESOLUTION & CONFIGURATION
# ==========================================
if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(os.path.abspath(sys.executable))
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

IMAGE_NAME = 'Scorch.png'
TEMPLATE_FILE = os.path.join(application_path, IMAGE_NAME)

KEY_CLOUDS = 18  
KEY_STINGERS = 19 
KEY_JELLYBEANS = 20 
X_PERCENT = 0.4464  
Y_PERCENT = 0.8686  

# ==========================================
# 2. MAC OS INJECTION LOGIC (HEURISTIC MASKING)
# ==========================================
CG = ctypes.cdll.LoadLibrary('/System/Library/Frameworks/CoreGraphics.framework/CoreGraphics')
CG.CGEventCreateKeyboardEvent.restype = ctypes.c_void_p
CG.CGEventCreateKeyboardEvent.argtypes = [ctypes.c_void_p, ctypes.c_uint16, ctypes.c_bool]
CG.CGEventPost.restype = None
CG.CGEventPost.argtypes = [ctypes.c_uint32, ctypes.c_void_p]
CFRelease = CG.CFRelease
CFRelease.argtypes = [ctypes.c_void_p]
CFRelease.restype = None

def human_sleep(target_time, max_variance):
    actual_time = target_time + random.uniform(-max_variance, max_variance)
    time.sleep(max(0.001, actual_time))

def mac_tap(keycode):
    event_down = CG.CGEventCreateKeyboardEvent(None, keycode, True)
    CG.CGEventPost(0, event_down)
    human_sleep(0.03, 0.005) 
    
    event_up = CG.CGEventCreateKeyboardEvent(None, keycode, False)
    CG.CGEventPost(0, event_up)
    
    CFRelease(event_down)
    CFRelease(event_up)

# ==========================================
# 3. UI & STATE MACHINE APPLICATION
# ==========================================
class MacroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Booster Macro v1.0")
        self.root.geometry("450x550")
        self.root.configure(padx=15, pady=15)
        
        self.is_running = threading.Event()
        self.is_running.clear()
        
        self.setup_ui()
        self.extract_baseline_color()
        
        threading.Thread(target=self.upkeep_stinger, daemon=True).start()
        threading.Thread(target=self.upkeep_jellybeans, daemon=True).start()
        threading.Thread(target=self.scan_scorch_activation, daemon=True).start()
        
        self.listener = keyboard.GlobalHotKeys({
            '<cmd>+<shift>+m': self.toggle_macro
        })
        self.listener.start()

    def extract_baseline_color(self):
        try:
            template_img = cv2.imread(TEMPLATE_FILE, cv2.IMREAD_COLOR)
            if template_img is None:
                raise FileNotFoundError
            self.target_color = np.mean(template_img, axis=(0, 1))
            self.log(f"System Ready. Target Color Loaded: {np.round(self.target_color, 1)}")
        except Exception:
            self.log(f"ERROR: Could not find '{IMAGE_NAME}'. Macro will fail.")
            self.target_color = np.array([0, 0, 0])

    def setup_ui(self):
        inst_frame = ttk.LabelFrame(self.root, text=" Instructions ")
        inst_frame.pack(fill="x", pady=(0, 10))
        instructions = (
            "1. Ensure Roblox is maximized / full-screen.\n"
            "2. IMPORTANT: ONLY START MACRO WHEN ROBLOX \nIS ON THE DISPLAY AND SCORCHING STAR IS \nOFF COOLDOWN!!\n"
            "3. Put stingers into slot 2, clouds/jellybeans into \nslots 1 and 3 (interchangable).\n"
            "4. Scorching star MUST be the 5th ability in your ability hotbar.\n"
            "5. Use Cmd+Shift+M anywhere to toggle the macro on/off.\n"
            "6. Keep this app running in the background.\n"
            "7. DM Discord @light_0912 for bugs or questions."
        )
        ttk.Label(inst_frame, text=instructions, justify="left").pack(padx=10, pady=5)
        
        self.status_label = tk.Label(self.root, text="STATUS: PAUSED", fg="red", font=("Helvetica", 16, "bold"))
        self.status_label.pack(pady=5)
        
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=5)
        self.start_btn = tk.Button(btn_frame, text="Start (Cmd+Shift+M)", command=self.start_macro, width=15, bg="#d4edda")
        self.start_btn.pack(side="left", padx=5)
        self.stop_btn = tk.Button(btn_frame, text="Stop (Cmd+Shift+M)", command=self.stop_macro, width=15, state="disabled", bg="#f8d7da")
        self.stop_btn.pack(side="left", padx=5)
        
        ttk.Label(self.root, text="Live Event Log:").pack(anchor="w")
        self.log_text = scrolledtext.ScrolledText(self.root, height=15, width=50, state="disabled", bg="#1e1e1e", fg="#00ff00")
        self.log_text.pack(fill="both", expand=True)

    def log(self, message):
        self.root.after(0, self._append_log, message)
        
    def _append_log(self, message):
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.config(state='normal')
        self.log_text.insert('end', f"[{timestamp}] {message}\n")
        self.log_text.see('end')
        self.log_text.config(state='disabled')

    def toggle_macro(self):
        if self.is_running.is_set():
            self.root.after(0, self.stop_macro)
        else:
            self.root.after(0, self.start_macro)

    def start_macro(self):
        self.is_running.set()
        self.status_label.config(text="STATUS: RUNNING & ARMED", fg="green")
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.log("Macro Armed. Monitoring display buffer...")

    def stop_macro(self):
        self.is_running.clear()
        self.status_label.config(text="STATUS: PAUSED", fg="red")
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.log("Macro Paused. Standing by.")

    # ==========================================
    # WORKER THREADS
    # ==========================================
    def upkeep_stinger(self):
        while True:
            self.is_running.wait()
            mac_tap(KEY_STINGERS)
            wait_time = 10.0 + random.uniform(-0.5, 0.5)
            end_time = time.time() + wait_time
            
            while time.time() < end_time:
                if not self.is_running.is_set():
                    break
                time.sleep(0.25)
                
    def upkeep_jellybeans(self):
        while True:
            self.is_running.wait()
            mac_tap(KEY_CLOUDS)
            wait_time = 30.5 + random.uniform(0.1, 0.5)
            end_time = time.time() + wait_time
            
            while time.time() < end_time:
                if not self.is_running.is_set():
                    break
                time.sleep(0.25)

    def scan_scorch_activation(self):
        base_is_visible = False 
        
        with mss.MSS() as sct:
            monitor = sct.monitors[1]
            screen_width = monitor["width"]
            screen_height = monitor["height"]
            
            # Reverted to original 1x1 pixel capture region
            calc_left = int(screen_width * X_PERCENT)
            calc_top = int(screen_height * Y_PERCENT)
            
            capture_region = {"top": calc_top, "left": calc_left, "width": 1, "height": 1}
            
            while True:
                if not self.is_running.is_set():
                    time.sleep(0.5)
                    continue

                screenshot = sct.grab(capture_region)
                img = np.array(screenshot)[:, :, :3] 
                
                current_color = np.mean(img, axis=(0, 1))
                color_diff = np.linalg.norm(self.target_color - current_color)
                
                is_match = color_diff < 30.0 

                if is_match:
                    if not base_is_visible:
                        self.log("Solid red base detected. Awaiting activation...")
                        base_is_visible = True
                        
                elif not is_match and base_is_visible:
                    self.log(f"Color shift detected (Delta: {color_diff:.2f}). Firing abilities!")
                    
                    mac_tap(KEY_JELLYBEANS)
                    human_sleep(0.05, 0.005) 
                    mac_tap(KEY_CLOUDS)
                    
                    self.log("Cooldown initiated (65s).")
                    base_is_visible = False 
                    
                    # Global cd
                    cooldown_end = time.time() + 65.0
                    while time.time() < cooldown_end:
                        if not self.is_running.is_set():
                            break
                        time.sleep(0.5) 

                human_sleep(0.1, 0.002)

if __name__ == "__main__":
    root = tk.Tk()
    app = MacroApp(root)
    
    def on_closing():
        app.stop_macro()
        root.destroy()
        sys.exit()
        
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.attributes('-topmost', True) 
    root.mainloop()
