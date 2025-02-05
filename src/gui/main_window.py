import tkinter as tk
from tkinter import ttk
import json
import requests
from tkinter import messagebox

# from config.config import load_config
from utils.updater import check_latest_version, install_update
from version.version import CURRENT_VERSION

from gui.view.log_viewer import LogViewer
from core.log.logger import logger
from core.schedule.task import start_scheduler


def on_check_update(root, CURRENT_VERSION="1.0.0"):
    latest_version, download_url = check_latest_version()
    if latest_version:
        if latest_version != CURRENT_VERSION:
            logger.info(f"A new version is available: {latest_version}")
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


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("SNS Analyzer")
        self.geometry("1000x600")

        # Sidebar frame
        self.sidebar = tk.Frame(self, bg="#F0F0F0", width=200)
        self.sidebar.pack(side="left", fill="y")
        
        tk.Label(self.sidebar, text="Valkyrie", font=("Arial", 14, "bold"), bg="#F0F0F0").pack(pady=10)
        
        self.menu_buttons = ["总览", "valkyrie设置", "通用设置", "直连设置", "主线图", "活动图", "工具"]
        for text in self.menu_buttons:
            ttk.Button(self.sidebar, text=text, width=15).pack(pady=2, padx=10, anchor="w")

        # Main Content Frame
        self.main_content = tk.Frame(self)
        self.main_content.pack(side="right", expand=True, fill="both")

        # Top Panel (Control and Logs)
        self.top_panel = tk.Frame(self.main_content)
        self.top_panel.pack(fill="x")
        
        ttk.Button(self.top_panel, text="启动").pack(side="left", padx=5, pady=5)
        ttk.Button(self.top_panel, text="停止").pack(side="left", padx=5, pady=5)
        # ttk.Button(self.top_panel, text="清空日志", command=self.clear_logs).pack(side="right", padx=5, pady=5)

        check_update_button = ttk.Button(self.top_panel, text="check_update", command=lambda: on_check_update(self, CURRENT_VERSION))
        check_update_button.pack(side="left", padx=5, pady=5)
        install_update_button = ttk.Button(self.top_panel, text="install_update", command=lambda: on_install_update(self))
        install_update_button.pack(side="left", padx=5, pady=5)

        # Logs Frame
        log_viewer = LogViewer(self.main_content)
        log_viewer.pack(expand=True, fill="both")

        # Start the scheduler
        start_scheduler()
        logger.info("GUI Initialized and Scheduler Running")
        