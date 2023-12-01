import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedStyle

class ConfigApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Configuration App")
        self.root.geometry("1200x600")

        self.configurations = {
            "General": {
                "Config1": {"status": False, "image": "general_image.png"},
                "Config2": {"status": False, "image": "general_image.png"},
            },
            "Advanced": {
                "Config3": {"status": False, "image": "advanced_image.png"},
                "Config4": {"status": False, "image": "advanced_image.png"},
            },
        }

        self.style = ThemedStyle(self.root)
        self.style.set_theme("equilux")  # Set the arc theme for a modern look

        self.create_ui()

    def create_ui(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)

        categories_tab = ttk.Frame(notebook)
        notebook.add(categories_tab, text="Categories")

        categories_panel = ttk.Treeview(categories_tab, columns=("Toggle",), show="tree", selectmode="none")
        categories_panel.heading("#0", text="Categories", anchor="w")
        categories_panel.heading("Toggle", text="Toggle", anchor="w")

        for category in self.configurations:
            categories_panel.insert("", "end", text=category, open=True)

        categories_panel.pack(side="left", fill="y", padx=10, pady=10)

        config_tab = ttk.Frame(notebook)
        notebook.add(config_tab, text="Configurations")

        self.config_panel = ttk.Treeview(config_tab, columns=("Config",), show="tree")
        self.config_panel.heading("#0", text="Configurations", anchor="w")
        self.config_panel.heading("Config", text="Config", anchor="w")

        config_frame_container = ttk.Frame(config_tab)
        config_frame_container.pack(side="left", fill="both", expand=True)

        for category, configs in self.configurations.items():
            for config, data in configs.items():
                config_frame = ttk.Frame(config_frame_container, style="Config.TFrame")  # Use a custom style for a modern look
                config_frame.grid(row=len(config_frame_container.winfo_children()), column=0, padx=5, pady=5, sticky="w")

                config_canvas = tk.Canvas(config_frame, width=200, height=150, bd=2, relief="solid", highlightthickness=0)
                config_canvas.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

                title_label = tk.Label(config_canvas, text=f"{config} Configuration", font=('Arial', 12, 'bold'), bg="#f0f0f0")
                title_label.grid(row=0, column=1, pady=(5, 0), sticky="w")

                image_path = data["image"]
                img = tk.PhotoImage(file=image_path)
                config_canvas.create_image(10, 10, anchor=tk.NW, image=img)

                config_button = ttk.Button(config_frame, text="Config", command=lambda category=category, config=config: self.show_config_frame(category, config))
                config_button.grid(row=1, column=0, pady=5, sticky="w")

        self.config_panel.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        save_button = ttk.Button(config_tab, text="Save Settings", command=self.save_settings)
        save_button.pack(pady=10)

        staff_tab = ttk.Frame(notebook)
        notebook.add(staff_tab, text="Staff")

        staff_label = tk.Label(staff_tab, text="Staff Information", font=('Arial', 16, 'bold'), bg="#ffcccc")
        staff_label.pack(pady=10)

        credits_tab = ttk.Frame(notebook)
        notebook.add(credits_tab, text="Credits")

        credits_label = tk.Label(credits_tab, text="Credits Information", font=('Arial', 16, 'bold'), bg="#ccffcc")
        credits_label.pack(pady=10)

        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=self.root.destroy)

        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Staff", command=lambda: notebook.select(staff_tab))
        help_menu.add_command(label="Credits", command=lambda: notebook.select(credits_tab))

        # Define a custom style for the Config frames
        self.style.configure("Config.TFrame", background="#f0f0f0", borderwidth=2, relief="solid")

    def show_config_frame(self, category, config):
        # Create a new window (Toplevel) for configuration
        config_window = tk.Toplevel(self.root)
        config_window.title(f"{config} Configuration")
        config_window.geometry("400x300")
        
        tk.Label(config_window, text=f"Name: {config}", font=('Arial', 14)).pack(pady=10)
        tk.Label(config_window, text="Description: This is a sample description.", font=('Arial', 12)).pack(pady=10)

        enable_disable_button = ttk.Button(config_window, text="Enable" if not self.configurations[category][config]["status"] else "Disable", command=lambda: self.toggle_config(category, config))
        enable_disable_button.pack(pady=10)

        save_button = ttk.Button(config_window, text="Save", command=lambda: self.save_config(category, config))
        save_button.pack(pady=10)

        back_button = ttk.Button(config_window, text="Back", command=config_window.destroy)
        back_button.pack(pady=10)
        ThemedStyle(config_window).set_theme("equilux")
        
    def save_settings(self):
        with open("settings.txt", "w") as file:
            for category, configs in self.configurations.items():
                file.write(f"[{category}]\n")
                for config, data in configs.items():
                    file.write(f"{config}={data['status']}\n")

        messagebox.showinfo("Saved", "Settings saved to settings.txt")

    def toggle_config(self, category, config):
        current_status = self.configurations[category][config]["status"]
        new_status = not current_status
        self.configurations[category][config]["status"] = new_status
        messagebox.showinfo("Status Changed", f"Status of {config} changed to {new_status}")

    def save_config(self, category, config):
        messagebox.showinfo("Config Saved", f"Configuration {config} in {category} saved.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ConfigApp(root)
    root.mainloop()
