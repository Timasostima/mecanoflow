from customtkinter import CTk, CTkToplevel, CTkFrame, CTkLabel
import customtkinter as ctk

from src.ui.charts import ChartFrame
from src.utils.system_appearence import detect_system_appearance
from src.ui.typing_app import TypingApp
from src.ui.app_bar import AppBar

themes = ["breeze", "coffee", "lavender", "marsh", "metal", "patina", "sky", "yellow"]


class Main(CTk):
    def __init__(self, theme_index=7):
        super().__init__()
        self.minsize(800, 350)
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme(f"res/themes/{themes[theme_index]}.json")
        self.title("MecanoFlow")

        self.theme_index = theme_index
        self.wpm_data = []
        self.acc_data = []
        self.errors_data = []

        # or simply by variable, but it doesn't work with system
        self.system_mode = detect_system_appearance()
        self.is_dark_mode = 1 if self.system_mode == "Dark" else 0

        self.app_bar = AppBar(self)
        self.app_bar.pack(fill='x')
        self.typing_app = TypingApp(self)
        self.typing_app.pack(expand=True, fill='both')

        self.after(5000, self.check_and_update_theme)
        # self.update_idletasks()
        # self.show_chart()

    def show_chart(self):
        toplevel = CTkToplevel(self, fg_color=ctk.ThemeManager.theme["CTkFrame"]["fg_color"][self.is_dark_mode])
        toplevel.geometry("1000x550")
        toplevel.resizable(False, False)
        toplevel.title("Chart")
        top_frame = CTkFrame(toplevel, fg_color=ctk.ThemeManager.theme["CTkFrame"]["fg_color"][self.is_dark_mode], corner_radius=0)
        top_frame.pack(fill='x')
        logo_label = CTkLabel(
            top_frame,
            image=self.app_bar.logo_image,
            text="",
        )
        logo_label.pack(pady=(7, 5), side='top')

        info = CTkFrame(toplevel, corner_radius=0, fg_color=ctk.ThemeManager.theme["CTkFrame"]["fg_color"][self.is_dark_mode])
        info.pack(side='left', expand=True)
        CTkLabel(
            info,
            text=self.typing_app.translations[1],
            font=("Arial", 20, "bold"),
            text_color=ctk.ThemeManager.theme["CTkLabel"]["text_color"][self.is_dark_mode]
        ).pack()
        CTkLabel(
            info,
            text=self.wpm_data[-1],
            font=("Arial", 60, "bold"),
            text_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"][self.is_dark_mode]
        ).pack(pady=(0, 20))
        CTkLabel(
            info,
            text=self.typing_app.translations[12],
            font=("Arial", 20, "bold"),
            text_color=ctk.ThemeManager.theme["CTkLabel"]["text_color"][self.is_dark_mode]
        ).pack()
        CTkLabel(
            info,
            text=f"{self.acc_data[-1]}%",
            font=("Arial", 60, "bold"),
            text_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"][self.is_dark_mode]
        ).pack()

        chart_frame = ChartFrame(
            toplevel, self.wpm_data, self.acc_data, self.errors_data,
            self.is_dark_mode, self.typing_app.translations
        )
        chart_frame.pack(expand=True, fill='both')

    def check_and_update_theme(self):
        system_theme = detect_system_appearance()
        if system_theme != self.system_mode:
            self.system_mode = system_theme
            self.is_dark_mode = 1 if system_theme == "Dark" else 0
            self.update_all_custom_colors()

        self.after(3000, self.check_and_update_theme)

    def update_all_custom_colors(self):
        self.typing_app.configure(fg_color=ctk.ThemeManager.theme["CTkFrame"]["fg_color"][self.is_dark_mode])
        self.typing_app.middleFrame.configure(border_color=ctk.ThemeManager.theme["CTkFrame"]["top_fg_color"][self.is_dark_mode])
        self.typing_app.words_conveyor.configure(fg_color=ctk.ThemeManager.theme["CTkFrame"]["fg_color"][self.is_dark_mode])
        self.typing_app.input_conveyor.configure(fg_color=ctk.ThemeManager.theme["CTkFrame"]["fg_color"][self.is_dark_mode])
        self.typing_app.entry.configure(fg=ctk.ThemeManager.theme["CTkLabel"]["text_color"][self.is_dark_mode])
        self.typing_app.entry.configure(bg=ctk.ThemeManager.theme["CTkFrame"]["fg_color"][self.is_dark_mode])
        self.typing_app.entry.configure(insertbackground=ctk.ThemeManager.theme["CTkLabel"]["text_color"][self.is_dark_mode])

        self.typing_app.topBar.container.configure(fg_color=ctk.ThemeManager.theme["CTkFrame"]["top_fg_color"][self.is_dark_mode])
        self.typing_app.topBar.update_subtype_colors(self.typing_app.topBar.selected_subtype)
        self.typing_app.topBar.update_restart_button()


if __name__ == "__main__":
    root = Main()
    root.mainloop()
