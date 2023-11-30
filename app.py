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
                "Config1": False,
                "Config2": False,
            },
            "Advanced": {
                "Config3": False,
                "Config4": False,
            },
            
        }

        
        style = ThemedStyle(self.root)
        style.set_theme("equilux")  

        
        self.create_ui()

    def create_ui(self):
        
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)

        
        categories_tab = ttk.Frame(notebook)
        notebook.add(categories_tab, text="Categories")

        
        categories_panel = ttk.Treeview(categories_tab, columns=("Status", "Toggle"), show="tree", selectmode="none")
        categories_panel.heading("#0", text="Categories", anchor="w")
        categories_panel.heading("Status", text="Status", anchor="w")
        categories_panel.heading("Toggle", text="Toggle", anchor="w")

        for category in self.configurations:
            categories_panel.insert("", "end", text=category, open=True)

        categories_panel.pack(side="left", fill="y", padx=10, pady=10)

        
        config_tab = ttk.Frame(notebook)
        notebook.add(config_tab, text="Configurations")

        
        self.config_panel = ttk.Treeview(config_tab, columns=("Status", "Toggle"), show="tree")
        self.config_panel.heading("#0", text="Configurations", anchor="w")
        self.config_panel.heading("Status", text="Status", anchor="w")
        self.config_panel.heading("Toggle", text="Toggle", anchor="w")

        for category, configs in self.configurations.items():
            category_item = self.config_panel.insert("", "end", text=category, open=True)
            for config, value in configs.items():
                status_item = self.config_panel.insert(category_item, "end", text=config, values=(str(value), ""))
                self.config_panel.tag_bind(status_item, '<1>', lambda event, config=config, item=status_item: self.on_treeview_click(event, config, item))

                
                toggle_button = ttk.Button(config_tab, text="Toggle", command=lambda config=config, item=status_item: self.toggle_config(config, item))
                toggle_button.pack(side="left", padx=5)

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

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Staff", command=lambda: notebook.select(staff_tab))
        help_menu.add_command(label="Credits", command=lambda: notebook.select(credits_tab))

    def save_settings(self):
        with open("settings.txt", "w") as file:
            for category, configs in self.configurations.items():
                file.write(f"[{category}]\n")
                for config, value in configs.items():
                    file.write(f"{config}={value}\n")

        messagebox.showinfo("Saved", "Settings saved to settings.txt")

    def on_treeview_click(self, event, config, item):
        category = self.config_panel.item(self.config_panel.parent(item))["text"]
        current_value = self.configurations[category][config]
        new_value = not current_value
        self.configurations[category][config] = new_value
        self.config_panel.item(item, values=(str(new_value), ""))  # Update the values directly
        print(f"Updated item values: {self.config_panel.item(item, 'values')}")

    def toggle_config(self, config, item):
        category = self.config_panel.item(self.config_panel.parent(item))["text"]
        current_value = self.configurations[category][config]
        new_value = not current_value
        self.configurations[category][config] = new_value
        self.config_panel.item(item, values=(str(new_value), ""))  # Update the values directly
        print(f"Toggled item values: {self.config_panel.item(item, 'values')}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ConfigApp(root)
    root.mainloop()
