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
                "Server Name": {
                    "status": False,
                    "image": "placeholder_image.png",
                    "properties": {
                        "Name": {"value": "text", "type": "text"},
                        "numberoftimesnamewillshow": {"value": 0, "type": "number"},
                        "enable_disable": {"value": False, "type": "boolean"},
                        "showname": {"value": True, "type": "boolean"},
                    },
                },
                "Police Job": {
                    "status": False,
                    "image": "placeholder_image.png",
                    "properties": {
                        "HandCuffKeys": {"value": "false", "type": "boolean"}
                        
                    },
                },
            },
            "Crime": {
                "Progress": {"status": False, "image": "placeholder_image.png", "type": "boolean"},
                "Art Robbery": {"status": False, "image": "placeholder_image.png", "type": "number"},
                "Bank Robbery": {"status": False, "image": "placeholder_image.png", "type": "text"},
            },
        }

        # self.configurations["Crime"]["Bank Robbery"]["properties"]["Required Cops Amount"] = {"value": 5, "type": "number"}
        
        self.configurations = self.load_configurations()

        self.style = ThemedStyle(self.root)
        self.style.set_theme("equilux")  

        self.create_ui()

     
    def load_configurations(self):
        configurations = {}

        try:
            with open("settings.txt", "r") as file:
                lines = file.readlines()
                current_category = None

                for line in lines:
                    line = line.strip()
                    if line.startswith("[") and line.endswith("]"):
                        current_category = line[1:-1]
                        configurations[current_category] = {}
                    elif ":" in line and current_category:
                        config, props_data = line.split(":", 1)
                        properties = {}

                        # Split properties
                        for prop_data in props_data.split(","):
                            prop_data = prop_data.strip()
                            if "=" in prop_data:
                                prop, value = prop_data.split("=")
                                prop_type = value.split(":")[-1].strip()  # Extract type from the value
                                properties[prop.strip()] = {"value": value.split(":")[0].strip(), "type": prop_type}

                        # Get image separately
                        image_data = properties.pop("image", {"value": "placeholder_image.png"})

                        configurations[current_category][config] = {
                            "status": True,  # Adjust this as needed
                            "image": image_data["value"],
                            "properties": properties,
                            "type": "boolean",  # Default to boolean, adjust as needed
                        }

        except FileNotFoundError:
            configurations = {
                "General": {
                    "Server Name": {
                        "status": False,
                        "image": "placeholder_image.png",
                        "properties": {
                            "Name": {"value": "", "type": "text"},
                            "numberoftimesnamewillshow": {"value": 0, "type": "number"},
                            "enable_disable": {"value": False, "type": "boolean"},
                            "showname": {"value": True, "type": "boolean"},
                        },
                    },
                    "Police Job": {"status": False, "image": "placeholder_image.png", "type": "boolean"},
                },
                "Crime": {
                    "Progress": {"status": False, "image": "placeholder_image.png", "type": "boolean"},
                    "Art Robbery": {"status": False, "image": "placeholder_image.png", "type": "number"},
                    "Bank Robbery": {"status": False, "image": "placeholder_image.png", "type": "text"},
                },
            }

        return configurations




    def validate_number(self, value):
        try:
            if value:
                float(value)
            return True
        except ValueError:
            return False
        
    def create_ui(self):
        # Load configurations before creating UI
        self.configurations = self.load_configurations()

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
                config_frame = ttk.Frame(config_frame_container, style="Config.TFrame")  
                config_frame.grid(row=len(config_frame_container.winfo_children()), column=0, padx=5, pady=5, sticky="w")
                properties = data.get("properties", {})
                data["properties"] = properties

                for prop_name, prop_type in properties.items():
                    if prop_type == "number":
                        prop_entry = ttk.Entry(config_frame, validate="key", validatecommand=(self.root.register(self.validate_number), "%P"))
                        prop_entry.grid(row=2, column=0, pady=5, padx=6, sticky="w")
                        data["properties"][prop_name] = prop_entry
                    elif prop_type == "text":
                        prop_entry = ttk.Entry(config_frame)
                        prop_entry.grid(row=2, column=0, pady=5, padx=6, sticky="w")
                        data["properties"][prop_name] = prop_entry
                # Add the appropriate widget based on the type
                if "type" in data and data["type"] == "boolean":
                    input_widget = ttk.Checkbutton(config_frame, text="Enable", variable=tk.BooleanVar(value=data["status"]))
                elif "type" in data and data["type"] == "text":
                    input_widget = ttk.Entry(config_frame)
                elif "type" in data and data["type"] == "number":
                    input_widget = ttk.Entry(config_frame, validate="key", validatecommand=(self.root.register(self.validate_number), "%P"))
                
        
                title_label = tk.Label(config_frame, text=f"{config} Configuration", font=('Arial', 12, 'bold'), bg="#f0f0f0")
                title_label.grid(row=0, column=0, pady=(5, 0), sticky="w")
                print(data)
                config_button = ttk.Button(
                config_frame,
                text="Config",
                command=lambda cat=category, conf=config, dat=data: self.show_config_frame(cat, conf, dat))

                config_button.grid(row=2, column=0, pady=5, padx=6, sticky="w")
        # input_widget.grid(row=1, column=0, pady=5, padx=6, sticky="w")
        self.config_panel.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        save_button = ttk.Button(config_tab, text="Save Settings", command=self.save_settings)
        save_button.pack(pady=7)

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

    def show_config_frame(self, category, config, data):
        config_window = tk.Toplevel(self.root)
        config_window.title(f"{config} Configuration")
        config_window.geometry("400x500")  # Increased height
        config_window.config(bg='#2e2e2e')  # Set to the desired background color
        ThemedStyle(config_window).set_theme("equilux")

        ttk.Label(config_window, text=f"Configuration: {config}", font=('Arial', 14), foreground='white', background='#2e2e2e').pack(pady=10)

        # Create a string to store configuration values
        config_values_str = ""

        for prop, prop_data in data.get("properties", {}).items():
            ttk.Label(config_window, text=f"{prop}:", font=('Arial', 12), foreground='white', background='#2e2e2e').pack(pady=5)

            # Determine type based on the input value
            prop_type = self.infer_type(prop_data["value"])

            if prop_type == "boolean":
                var = tk.BooleanVar(value=prop_data["value"].lower() == "true")
                input_widget = ttk.Checkbutton(config_window, text="Enabled" if var.get() else "Disabled", variable=var, style="Dark.TCheckbutton")
            elif prop_type == "text":
                var = tk.StringVar(value=prop_data["value"])
                input_widget = ttk.Entry(config_window, textvariable=var, style="Dark.TEntry")
            elif prop_type == "number":
                var = tk.StringVar(value=prop_data["value"])
                input_widget = ttk.Entry(config_window, validate="key", validatecommand=(self.root.register(self.validate_number), "%P"), textvariable=var, style="Dark.TEntry")

            input_widget.pack(pady=3, padx=10)  # Adjusted pady and padx

            # Append the configuration value to the string
            if prop_type == "boolean":
                config_values_str += f"{prop}: {var.get()}\n"
            else:
                config_values_str += f"{prop}: {var.get()}\n"  # Use var.get() for Entry widgets

        # Buttons Section
        buttons_frame = ttk.Frame(config_window)
        buttons_frame.pack(pady=10)

        enable_disable_button = ttk.Button(buttons_frame, text="Enable" if not data["status"] else "Disable", command=lambda: self.toggle_config(category, config), style="Dark.TButton")
        enable_disable_button.pack(side=tk.LEFT, padx=5)  # Adjusted padx
        save_button = ttk.Button(
            buttons_frame,
            text="Save",
            command=lambda cat=category, conf=config, dat=data, input_widget=input_widget: self.save_configuration(cat, conf, dat, input_widget)
        )

        save_button.pack(side=tk.LEFT, padx=5)  # Adjusted padx

        back_button = ttk.Button(buttons_frame, text="Back", command=config_window.destroy, style="Dark.TButton")
        back_button.pack(side=tk.LEFT, padx=5)  # Adjusted padx

        # Display Section
        ttk.Label(config_window, text="Configuration Values:", font=('Arial', 14), foreground='white', background='#2e2e2e').pack(pady=10)
        config_values_display = tk.Text(config_window, height=5, width=40, wrap=tk.WORD, background='#2e2e2e', foreground='white', insertbackground='white')
        config_values_display.insert(tk.END, config_values_str)
        config_values_display.pack(pady=5)

        # Disable text widget editing
        config_values_display.config(state=tk.DISABLED)

        # Themed style for custom widgets
        style = ThemedStyle(config_window)
        style.set_theme("equilux")

        # Custom style for Checkbutton and Entry
        style.configure("Dark.TCheckbutton", background='#2e2e2e', foreground='white')
        style.configure("Dark.TEntry", fieldbackground='#2e2e2e', foreground='white')

        # Custom style for Buttons
        style.configure("Dark.TButton", background='#2e2e2e', foreground='white', padding=5, font=('Arial', 10, 'bold'))


    def infer_type(self, value):
        if value.lower() == "true" or value.lower() == "false":
            return "boolean"
        elif value.isdigit():
            return "number"
        else:
            return "text"

            
    def save_settings(self):
        with open("settings.txt", "w") as file:
            for category, configs in self.configurations.items():
                file.write(f"[{category}]\n")
                for config, data in configs.items():
                    file.write(f"{config}={data['status']}\n")

        messagebox.showinfo("Saved", "Settings saved to settings.txt")

        
    def save_configuration(self, category, config, data, input_widgets):
        # Get the current settings
        with open('settings.txt', 'r') as file:
            lines = file.readlines()

        # Update the settings
        value = None  # Default value if not assigned within the loop
        for i, line in enumerate(lines):
            if line.startswith(f"{config}="):
                # Extract the current type
                current_type = self.extract_type(line)

                # Determine the type of the configuration
                if current_type == 'boolean':
                    # For boolean, update the value based on the state of the checkbutton
                    value = "True" if input_widgets.get() else "False"
                elif current_type == 'number':
                    # For text and number, get the value from the input widget
                    value = input_widgets.get()

                # Update the line with the new value
                lines[i] = f"{config}={value}, type={current_type}\n"
                break

        # Save the updated settings back to the file
        with open('settings.txt', 'w') as file:
            file.writelines(lines)

        print(f"Configuration '{config}' updated successfully with value '{value}'.")




    def extract_value_and(self, line):
        # Extract value and type from a line in the settings file
        parts = line.strip().split('=')
        config_value = parts[1].split(',')[0].strip()
        return config_value

    def extract_type(self, line):
        type_start = line.find("type=") + len("type=")
        type_end = line.find(",", type_start)
        return line[type_start:type_end].strip()

if __name__ == "__main__":
    root = tk.Tk()
    app = ConfigApp(root)
    root.mainloop()
