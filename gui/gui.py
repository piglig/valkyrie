import tkinter as tk
import json
import requests
from tkinter import messagebox
from config.config import load_config
from utils.updater import check_latest_version, install_update

def on_check_update(root):
    latest_version, download_url = check_latest_version()
    if latest_version:
        if latest_version != CURRENT_VERSION:
            messagebox.showinfo("Update Available", f"A new version is available: {latest_version}")
            # Optionally, store the download URL in a global variable for use when installing update
            root.download_url = download_url
        else:
            messagebox.showinfo("No Update", "You are already using the latest version.")


def on_install_update(root):
    # Check if download_url was set previously from check_update
    download_url = getattr(root, "download_url", None)
    if not download_url:
        messagebox.showinfo("Install Update", "Please check for an update first.")
        return

    # Confirm installation with the user
    if messagebox.askyesno("Install Update", "Do you want to download and install the update?"):
        install_update(download_url)

def create_gui():
    # Create the main window
    root = tk.Tk()
    root.title("GitHub Updater App")
    root.geometry("300x200")

    # Load the JSON configuration
    config = load_config()
    if config is None:
        return

    # Create a dictionary to map button names to functions
    button_actions = {
        "check_update": lambda: on_check_update(root),
        "install_update": lambda: on_install_update(root)
    }

    # Create buttons based on the JSON config
    for btn_conf in config.get("buttons", []):
        name = btn_conf.get("name")
        text = btn_conf.get("text", "Button")
        pos = btn_conf.get("position", {"x": 0, "y": 0})
        size = btn_conf.get("size", {"width": 80, "height": 30})

        btn = tk.Button(root, text=text)
        # Set the button’s command if it exists in our dictionary
        if name in button_actions:
            btn.config(command=button_actions[name])
        # Place the button on the window
        btn.place(x=pos.get("x", 0),
                  y=pos.get("y", 0),
                  width=size.get("width", 80),
                  height=size.get("height", 30))

    return root
