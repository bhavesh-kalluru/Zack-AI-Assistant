import tkinter as tk
from tkinter import ttk
import subprocess
import webbrowser
import urllib.parse
import re
import threading
import openai
import os
from dotenv import load_dotenv
from PIL import Image, ImageTk

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

APP_ALIASES = {
    "outlook": "Microsoft Outlook",
    "word": "Microsoft Word",
    "excel": "Microsoft Excel",
    "powerpoint": "Microsoft PowerPoint",
    "chrome": "Google Chrome",
    "safari": "Safari",
    "calculator": "Calculator",
    "notes": "Notes",
    "terminal": "Terminal",
    "mail": "Mail",
    "finder": "Finder",
    "calendar": "Calendar",
}

TASKS = []

THEMES = {
    "dark": {"bg": "#121212", "fg": "#e0e0e0"},
    "light": {"bg": "#f5f5f5", "fg": "#111111"}
}

current_theme = "dark"

def open_app(app_name):
    app_key = app_name.lower().strip()
    app_to_open = APP_ALIASES.get(app_key, None)
    if not app_to_open:
        app_to_open = " ".join(word.capitalize() for word in app_name.split())

    if app_key in ["amazon", "youtube", "linkedin", "google"]:
        return f"❌ '{app_key}' is a website, not a macOS application. Try: 'search shoes on amazon'."

    try:
        subprocess.run(["open", "-a", app_to_open], check=True)
        return f"✅ Opening {app_to_open}."
    except subprocess.CalledProcessError:
        return f"❌ Could not open app '{app_name}'. Please check the name."

def open_url_threaded(url):
    def open():
        try:
            webbrowser.open(url, new=2)
        except Exception as e:
            print("Failed to open URL:", e)
    threading.Thread(target=open, daemon=True).start()

def open_website_search(site, query):
    base_urls = {
        "amazon": "https://www.amazon.com/s?k=",
        "youtube": "https://www.youtube.com/results?search_query=",
        "linkedin": "https://www.linkedin.com/search/results/all/?keywords=",
        "google": "https://www.google.com/search?q="
    }
    if site in base_urls:
        url = base_urls[site] + urllib.parse.quote(query)
        open_url_threaded(url)
        return f"🌐 Searching {site.capitalize()} for '{query}'."
    else:
        return f"❌ Unsupported website: {site}"

def is_app_command(text):
    return bool(re.match(r'^\s*open\s+[a-zA-Z0-9 ._-]+', text.lower()))

def is_web_command(text):
    return bool(re.search(r'(search|find).*on\s+(youtube|amazon|linkedin|google)', text.lower()))

def extract_web_query(text):
    match = re.search(r'(?:search|find)\s+(.*?)\s+on\s+(youtube|amazon|linkedin|google)', text.lower())
    if match:
        query = match.group(1).strip()
        site = match.group(2).strip()
        return site, query
    return None, None

def fallback_with_gpt(user_input):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are Zack, an intelligent desktop assistant that helps users open apps and search the web."},
                {"role": "user", "content": user_input}
            ],
            max_tokens=60,
            temperature=0.5
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ GPT failed to respond: {str(e)}"

def process_command(command):
    command = command.strip()
    command_lower = command.lower()

    if command_lower.startswith("add task"):
        task = command[8:].strip()
        if task:
            TASKS.append(task)
            return f"✅ Task added: {task}"
        else:
            return "⚠️ Please specify a task after 'add task'"

    if command_lower in ["show tasks", "list tasks"]:
        if TASKS:
            return "📝 Tasks:\n" + "\n".join(f"- {task}" for task in TASKS)
        else:
            return "📝 No tasks added yet."

    if is_app_command(command):
        match = re.match(r'open\s+([a-zA-Z0-9 ._-]+)', command_lower)
        if match:
            return open_app(match.group(1).strip())

    if is_web_command(command):
        site, query = extract_web_query(command)
        if site and query:
            return open_website_search(site, query)

    return fallback_with_gpt(command)

class ZackAssistant(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ZACK")
        self.geometry("900x500")
        self.resizable(False, False)

        # ✅ Dynamically resolve path to bg.png
        base_dir = os.path.dirname(os.path.abspath(__file__))
        bg_path = os.path.join('/Users/bhavi/Zack/assets/avatar:bg.png')

        # ✅ Set background image
        self.canvas = tk.Canvas(self, width=900, height=500)
        self.canvas.pack(fill="both", expand=True)
        self.bg_image = ImageTk.PhotoImage(Image.open(bg_path).resize((900, 500)))
        self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

        self.configure_ui()
        self.create_widgets()

    def configure_ui(self):
        theme = THEMES[current_theme]
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.style.configure('TLabel', background=theme["bg"], foreground=theme["fg"], font=("Segoe UI", 13))
        self.style.configure('TButton', font=("Segoe UI", 12), padding=6)
        self.style.configure('TEntry', font=("Segoe UI", 14))

    def toggle_theme(self):
        global current_theme
        current_theme = "light" if current_theme == "dark" else "dark"
        self.configure_ui()
        self.update_widgets_theme()

    def update_widgets_theme(self):
        theme = THEMES[current_theme]
        self.style.configure('TLabel', background=theme["bg"], foreground=theme["fg"])
        self.output_label.configure(background=theme["bg"], foreground=theme["fg"])

    def create_widgets(self):
        self.main_frame = tk.Frame(self.canvas, bg="", highlightthickness=0)
        self.main_window = self.canvas.create_window(0, 0, anchor="nw", window=self.main_frame, width=900, height=500)

        top_frame = ttk.Frame(self.main_frame)
        top_frame.pack(pady=12)

        title_label = ttk.Label(top_frame, text="ZACK", font=("Segoe UI", 22, "bold"))
        title_label.pack(side=tk.LEFT, padx=10)

        theme_btn = ttk.Button(top_frame, text="Toggle Theme", command=self.toggle_theme)
        theme_btn.pack(side=tk.RIGHT)

        center_frame = ttk.Frame(self.main_frame)
        center_frame.pack(pady=10, padx=10, fill='both', expand=True)

        self.output_var = tk.StringVar()
        self.output_label = ttk.Label(
            center_frame, textvariable=self.output_var, wraplength=500,
            anchor="center", justify="center", font=("Segoe UI", 13, "italic")
        )
        self.output_label.pack(pady=(10, 10), padx=20, side=tk.LEFT, expand=True)

        self.task_box = tk.Listbox(center_frame, height=15, width=30, font=("Segoe UI", 11))
        self.task_box.pack(side=tk.RIGHT, padx=10)
        self.update_task_box()

        bottom_frame = ttk.Frame(self.main_frame)
        bottom_frame.place(relx=0.5, rely=0.95, anchor='s')

        self.entry = ttk.Entry(bottom_frame, width=60)
        self.entry.grid(row=0, column=0, padx=(0, 10))
        self.entry.bind("<Return>", self.on_enter)

        send_button = ttk.Button(bottom_frame, text="Send", command=self.on_enter)
        send_button.grid(row=0, column=1)

        self.entry.focus()

    def update_task_box(self):
        self.task_box.delete(0, tk.END)
        for task in TASKS:
            self.task_box.insert(tk.END, f"- {task}")

    def on_enter(self, event=None):
        user_command = self.entry.get()
        if not user_command.strip():
            self.output_var.set("⚠️ Please enter a command or product.")
            return
        response = process_command(user_command)
        self.output_var.set(response)
        self.update_task_box()
        self.entry.delete(0, tk.END)

if __name__ == "__main__":
    app = ZackAssistant()
    app.mainloop()
