from customtkinter import CTkLabel, CTkFrame, CTkButton
import json
import os


def get_theme_hover_color(theme):
    theme_file = f'res/themes/{theme}.json'
    if os.path.exists(theme_file):
        with open(theme_file, 'r') as file:
            theme_data = json.load(file)
            return theme_data.get("CTkButton", {}).get("hover_color", ["#cccccc", "#333333"])[0]
    return "#cccccc"


def get_theme_color(theme):
    theme_file = f'res/themes/{theme}.json'
    if os.path.exists(theme_file):
        with open(theme_file, 'r') as file:
            theme_data = json.load(file)
            return theme_data.get("CTkButton", {}).get("fg_color", ["#ffffff", "#000000"])[0]
    return "#ffffff"


class ThemeChooser(CTkFrame):
    def __init__(self, master, themes, callback):
        super().__init__(master)
        self.callback = callback
        self.pack(expand=True, fill='both')

        self.label = CTkLabel(self, text="Select a Theme", font=("Arial", 30, "bold"))
        self.label.pack(pady=(30, 40))

        self.button_frame = CTkFrame(self)
        self.button_frame.pack()

        for i, theme in enumerate(themes):
            button = CTkButton(
                self.button_frame,
                text=theme.capitalize(),
                command=lambda t=theme: self.select_theme(t),
                font=("Arial", 15, "bold"),
                fg_color=get_theme_color(theme),
                hover_color=get_theme_hover_color(theme),
                corner_radius=10,
                height=50
            )
            button.grid(row=i // 3, column=i % 3, padx=10, pady=10)

    def select_theme(self, theme):
        self.callback(theme)
