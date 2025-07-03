import os
import webbrowser
from assistant.memory import show_recent

def execute_action(result):
    action = result.get("action")
    params = result.get("parameters", {})

    if action == "open_app":
        return open_app(params.get("name", ""))
    elif action == "play_music":
        return play_music()
    elif action == "create_folder":
        return create_folder(params.get("name", ""))
    elif action == "search_web":
        return search_web(params.get("query", ""))
    elif action == "show_recent":
        return show_recent()
    else:
        return "❌ I didn't understand that command."

def open_app(name):
    apps = {
        "youtube": "https://youtube.com",
        "amazon": "https://amazon.com",
        "safari": "open -a Safari",
        "music": "open -a Music",
        "whatsapp": "open -a WhatsApp"
    }
    key = name.lower()
    if key in apps:
        if apps[key].startswith("http"):
            webbrowser.open(apps[key])
        else:
            os.system(apps[key])
        return f"✅ Opened {name}"
    return f"❌ Unknown app: {name}"

def play_music():
    os.system("open -a Music")
    return "🎵 Music app opened"

def create_folder(name):
    try:
        path = os.path.expanduser(f"~/Desktop/{name}")
        os.makedirs(path, exist_ok=True)
        return f"📁 Folder created: {path}"
    except Exception as e:
        return f"❌ Error: {e}"

def search_web(query):
    webbrowser.open(f"https://www.google.com/search?q={query}")
    return f"🔍 Searching for: {query}"
