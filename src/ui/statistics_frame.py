from tkinter import StringVar

import customtkinter as ctk
from customtkinter import CTkFrame, CTkLabel

from src.ui.tooltip import ToolTip


class StatsFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.grid_columnconfigure(1, weight=1)
        self.configure(
            corner_radius=10,
            border_width=2,
            fg_color=ctk.ThemeManager.theme["CTkFrame"]["top_fg_color"],
        )

        # Add "WPM" Display
        self.wpm_value = StringVar(value="0.00")
        self.wpm_label = CTkLabel(self, textvariable=self.wpm_value, font=("Arial", 30, "bold"))
        self.wpm_label.grid(row=0, column=0, columnspan=2, pady=(10, 5), sticky="n")

        self.wpm_text = CTkLabel(self, text=f"{parent.translations[1]}", font=("Arial", 14), cursor="question_arrow")  # wpm
        self.wpm_tooltip = ToolTip(self.wpm_text, text="Words Per Minute")
        self.wpm_text.grid(row=1, column=0, columnspan=2, pady=(0, 10), sticky="n")

        # Stat variables
        self.character_accuracy = StringVar(value="100.00%")
        self.word_accuracy = StringVar(value="100.00%")
        self.word_list = StringVar(value="English")
        self.word_mode = StringVar(value="Time")
        self.incorrect_words = StringVar(value="0")

        # List of stats
        stats = [
            (f"{parent.translations[2]}", self.character_accuracy), # Character accuracy
            (f"{parent.translations[3]}", self.word_accuracy),  # Word accuracy
            (f"{parent.translations[4]}", self.word_list),  # Word list
            (f"{parent.translations[5]}", self.word_mode),  # Word mode
            (f"{parent.translations[6]}", self.incorrect_words)  # Incorrect words
        ]

        # Add stats labels
        for i, (stat_name, stat_value) in enumerate(stats, start=2):
            stat_label = CTkLabel(self, text=stat_name, font=("Arial", 14))
            stat_label.grid(row=i, column=0, padx=(10, 35), pady=5, sticky="w")

            value_label = CTkLabel(self, textvariable=stat_value, font=("Arial", 14))
            value_label.grid(row=i, column=1, padx=(5, 10), pady=5, sticky="e")

    def reset_stats(self):
        self.wpm_value.set("0.00")

        self.character_accuracy.set("100.00%")
        self.word_accuracy.set("100.00%")


