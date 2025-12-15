import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import os
import threading
import queue

# --- CONFIGURATION & STYLING ---
THUMBNAIL_SIZE = (70, 70) 
FONT_HEADER = ("Segoe UI", 9, "bold")
FONT_ROW = ("Segoe UI", 10)
FONT_ENTRY = ("Segoe UI", 10)

# Colors
COLOR_HEADER_BG = "#2c3e50"     # Dark Blue Header
COLOR_HEADER_FG = "white"
COLOR_BG_MAIN = "#ecf0f1"       # App Background
COLOR_ROW_EVEN = "white"
COLOR_ROW_ODD = "#f7f9f9"
COLOR_CTRL_BG = "#bdc3c7"       # Control Panel Background

# Column Configuration (Title, Min-Width, Weight)
# Weight 0 = Fixed width, Weight > 0 = Expandable
COL_CONFIG = [
    ("#", 40, 0),               # 0: Index
    ("IMAGE", 90, 0),           # 1: Image Thumbnail
    ("CURRENT NAME", 200, 1),   # 2: Old Filename
    ("NEW NAME", 250, 2),       # 3: New Filename Input
    ("LEN", 50, 0),             # 4: Char Counter
    ("STATUS", 120, 0)          # 5: Status/Error Message
]

class BatchRenameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Batch Rename Tool 2.0 - Visual Editor")
        
        # Center the window (1200x800)
        self.center_window(1200, 800)
        
        self.image_list = [] 
        self.load_queue = queue.Queue()
        
        self.setup_ui()
        
        # Start queue checker for smooth loading
        self.root.after(100, self.process_load_queue)

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{int(x)}+{int(y)}')

    def setup_ui(self):
        # --- 1. Control Panel (CENTERED) ---
        control_frame = tk.Frame(self.root, pady=15, bg=COLOR_CTRL_BG)
        control_frame.pack(fill=tk.X, side=tk.TOP)
        
        # Container to center buttons
        center_btn_container = tk.Frame(control_frame, bg=COLOR_CTRL_BG)
        center_btn_container.pack(anchor="center")
        
        # Common button style
        btn_style = {'font': ("Segoe UI", 9, "bold"), 'padx': 20, 'pady': 6, 'bd': 1, 'relief': 'raised', 'cursor': 'hand2'}
        
        # Action Buttons (Equal Spacing)
        tk.Button(center_btn_container, text="📂 Select Folder", command=self.browse_folder, bg="#3498db", fg="white", **btn_style).pack(side=tk.LEFT, padx=5)
        tk.Button(center_btn_container, text="📋 Paste List", command=self.paste_names, bg="#f39c12", fg="white", **btn_style).pack(side=tk.LEFT, padx=5)
        tk.Button(center_btn_container, text="🧹 Clear All", command=self.clear_inputs, bg="#95a5a6", fg="white", **btn_style).pack(side=tk.LEFT, padx=5)
        tk.Button(center_btn_container, text="▶ START RENAME", command=self.rename_all, bg="#27ae60", fg="white", **btn_style).pack(side=tk.LEFT, padx=5)

        # --- 2. Main List Area ---
        self.main_container = tk.Frame(self.root, bg=COLOR_BG_MAIN)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # HEADER FRAME
        self.header_frame = tk.Frame(self.main_container, bg=COLOR_HEADER_BG)
        self.header_frame.pack(fill=tk.X)
        
        # Create Header Columns using Grid Uniformity
        for i, (text, min_w, weight) in enumerate(COL_CONFIG):
            lbl = tk.Label(self.header_frame, text=text, fg=COLOR_HEADER_FG, bg=COLOR_HEADER_BG, font=FONT_HEADER, pady=8)
            lbl.grid(row=0, column=i, sticky="ew")
            # 'uniform' ensures alignment with the body rows below
            self.header_frame.grid_columnconfigure(i, weight=weight, minsize=min_w, uniform=f"col_{i}")

        # Dummy Column for Scrollbar offset (approx 17px)
        tk.Frame(self.header_frame, width=17, bg=COLOR_HEADER_BG).grid(row=0, column=len(COL_CONFIG))

        # CONTENT AREA (Canvas + Scrollbar)
        self.canvas = tk.Canvas(self.main_container, bg="white", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.main_container, orient="vertical", command=self.canvas.yview)
        
        self.scrollable_frame = tk.Frame(self.canvas, bg="white")
        
        # Sync Column Config for Body
        for i, (_, min_w, weight) in enumerate(COL_CONFIG):
            self.scrollable_frame.grid_columnconfigure(i, weight=weight, minsize=min_w, uniform=f"col_{i}")

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Sync Canvas Width on resize
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        
        # Bind Mouse Scrolling
        self.bind_mouse_scroll(self.canvas)
        self.bind_mouse_scroll(self.scrollable_frame)

    def on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def bind_mouse_scroll(self, widget):
        widget.bind("<MouseWheel>", self._on_mousewheel)
        widget.bind("<Button-4>", self._on_mousewheel)
        widget.bind("<Button-5>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        if event.num == 5 or event.delta == -120:
            self.canvas.yview_scroll(1, "units")
        elif event.num == 4 or event.delta == 120:
            self.canvas.yview_scroll(-1, "units")

    # --- LOGIC ---

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if not folder: return
        
        # Clear existing widgets
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.image_list.clear()
        
        # Start loading thread
        threading.Thread(target=self.load_images_thread, args=(folder,), daemon=True).start()

    def load_images_thread(self, folder):
        try:
            files = [f for f in os.listdir(folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp'))]
            files.sort()
            for idx, filename in enumerate(files):
                self.load_queue.put({
                    "id": idx + 1,
                    "full_path": os.path.join(folder, filename),
                    "filename": filename
                })
        except Exception as e:
            print(f"Error loading files: {e}")

    def process_load_queue(self):
        try:
            while True:
                item_data = self.load_queue.get_nowait()
                self.create_row(item_data)
        except queue.Empty:
            pass
        finally:
            self.root.after(100, self.process_load_queue)

    def create_row(self, item_data):
        row_idx = item_data["id"]
        bg_color = COLOR_ROW_EVEN if row_idx % 2 == 0 else COLOR_ROW_ODD
        
        # 0. Index
        tk.Label(self.scrollable_frame, text=str(row_idx), bg=bg_color, fg="gray").grid(row=row_idx, column=0, sticky="ns")

        # 1. Image Thumbnail
        img_lbl = tk.Label(self.scrollable_frame, text="", bg=bg_color, height=4) 
        img_lbl.grid(row=row_idx, column=1, pady=4)
        threading.Thread(target=self.load_thumbnail, args=(img_lbl, item_data["full_path"]), daemon=True).start()

        # 2. Current Name
        tk.Label(self.scrollable_frame, text=item_data["filename"], bg=bg_color, anchor="w", padx=10).grid(row=row_idx, column=2, sticky="ew")

        # 3. New Name Entry
        new_name_var = tk.StringVar()
        entry = tk.Entry(self.scrollable_frame, textvariable=new_name_var, font=FONT_ENTRY, bg="white", relief="solid", bd=1)
        entry.grid(row=row_idx, column=3, sticky="ew", padx=10, pady=15, ipady=3)
        
        # Keyboard Navigation
        entry.bind("<Return>", lambda e: self.focus_next_entry(e.widget))
        entry.bind("<Down>", lambda e: self.focus_next_entry(e.widget))
        entry.bind("<Up>", lambda e: self.focus_prev_entry(e.widget))

        # 4. Length Counter
        len_lbl = tk.Label(self.scrollable_frame, text="0", bg=bg_color, fg="#7f8c8d")
        len_lbl.grid(row=row_idx, column=4, sticky="ew")

        # 5. Status
        status_lbl = tk.Label(self.scrollable_frame, text="", bg=bg_color, font=("Segoe UI", 9))
        status_lbl.grid(row=row_idx, column=5, sticky="ew")

        # Live Validation
        def on_change(*args):
            text = new_name_var.get()
            len_lbl.config(text=str(len(text)))
            # Check for invalid Windows filename characters
            if any(c in r'\/:*?"<>|' for c in text):
                status_lbl.config(text="Invalid Char!", fg="#c0392b")
                entry.config(bg="#f9e79f")
            else:
                status_lbl.config(text="", fg="black")
                entry.config(bg="white")

        new_name_var.trace("w", on_change)

        self.image_list.append({
            "full_path": item_data["full_path"],
            "filename": item_data["filename"],
            "new_name_var": new_name_var,
            "status_lbl": status_lbl,
            "entry": entry
        })

    def load_thumbnail(self, lbl, path):
        try:
            img = Image.open(path)
            img.thumbnail(THUMBNAIL_SIZE)
            photo = ImageTk.PhotoImage(img)
            def update():
                lbl.config(image=photo, width=0, height=0)
                lbl.image = photo # Keep reference
            self.root.after(0, update)
        except: pass

    def focus_next_entry(self, widget):
        widget.tk_focusNext().focus()
        return "break"

    def focus_prev_entry(self, widget):
        widget.tk_focusPrev().focus()
        return "break"

    def paste_names(self):
        try:
            lines = [l.strip() for l in self.root.clipboard_get().splitlines() if l.strip()]
            for i, line in enumerate(lines):
                if i < len(self.image_list):
                    self.image_list[i]["new_name_var"].set(line)
        except: pass

    def clear_inputs(self):
        for item in self.image_list: item["new_name_var"].set("")

    def rename_all(self):
        count = 0
        err = 0
        
        # Pre-check for duplicate inputs
        inputs = [i["new_name_var"].get().strip() for i in self.image_list if i["new_name_var"].get().strip()]
        if len(inputs) != len(set(inputs)):
            messagebox.showwarning("Warning", "Duplicate names detected in your input list!")
            return

        for item in self.image_list:
            new_base = item["new_name_var"].get().strip()
            if not new_base: continue
            
            # Skip invalid characters
            if any(c in r'\/:*?"<>|' for c in new_base): continue

            old = item["full_path"]
            folder = os.path.dirname(old)
            ext = os.path.splitext(item["filename"])[1]
            new_name = new_base + ext
            new_full = os.path.join(folder, new_name)

            if new_name == item["filename"]: continue

            try:
                if os.path.exists(new_full):
                    item["status_lbl"].config(text="File Exists!", fg="red")
                    err += 1
                else:
                    os.rename(old, new_full)
                    # Update internal data
                    item["full_path"] = new_full
                    item["filename"] = new_name
                    # Update UI
                    item["status_lbl"].config(text="Success", fg="#27ae60")
                    count += 1
            except Exception as e:
                item["status_lbl"].config(text="Error", fg="red")
                err += 1
        
        messagebox.showinfo("Result", f"Renamed: {count}\nErrors: {err}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BatchRenameApp(root)
    root.mainloop()