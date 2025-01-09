import random
import time

from customtkinter import CTkFrame, CTkLabel
import customtkinter as ctk

from src.utils.Images import load_svg_image, img_to_ctk
from src.utils.config import languages
from src.utils.extracted_lists import get_language_list, get_translations
from src.ui.tooltip import ToolTip


class TopBar(CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.round_time = 30
        self.words_needed = 10
        self.time_left = self.round_time
        self.timer_running = False
        self.progress_label = CTkLabel(self, text=f"{self.time_left}s", font=('Arial', 30, 'bold'))
        self.progress_label.pack(side="bottom", pady=(2, 5))

        # Create a container frame inside the TopBar
        self.container = CTkFrame(
            self,
            fg_color=ctk.ThemeManager.theme["CTkFrame"]["top_fg_color"]
        )
        self.container.place(relx=0.5, rely=0.5, anchor="center")

        self.create_container_widgets()

    def create_container_widgets(self):
        self.selected_type = 0
        self.selected_subtype = 0

        self.time_type = CTkLabel(
            self.container,
            text="Time",
            font=('Arial', 15),
            cursor="hand2",
            text_color=ctk.ThemeManager.theme["CTkLabel"]["text_color"][self.parent.parent.is_dark_mode]
        )
        self.time_type.pack(side="left", padx=(25, 10), pady=10)
        self.time_type.bind("<Button-1>", lambda e: self.on_type_click(self.time_type))
        self.parent.parent.bind("<Control-t>", lambda e: self.on_type_click(self.time_type))
        ToolTip(self.time_type, text="Ctrl+T")

        self.words_type = CTkLabel(
            self.container,
            text="Words",
            font=('Arial', 15),
            cursor="hand2",
            text_color=ctk.ThemeManager.theme["CTkLabel"]["text_color"][self.parent.parent.is_dark_mode]
        )
        self.words_type.pack(side="left", padx=10, pady=10)
        self.words_type.bind("<Button-1>", lambda e: self.on_type_click(self.words_type))
        self.parent.parent.bind("<Control-w>", lambda e: self.on_type_click(self.words_type))
        ToolTip(self.words_type, text="Ctrl+W")

        self.original_restart_image = load_svg_image(
            "res/retry.svg",
            (20, 20),
            ctk.ThemeManager.theme["CTkLabel"]["text_color"][self.parent.parent.is_dark_mode]
        )
        self.restart_image = img_to_ctk(self.original_restart_image)
        self.restart_label = CTkLabel(
            self.container,
            image=self.restart_image,
            text="",
            cursor="hand2"
        )
        self.restart_label.pack(side="left", padx=10, pady=10)
        self.restart_tooltip = ToolTip(self.restart_label, text="Restart the test, Ctrl+R", delay=1500)

        self.restart_label.bind("<Button-1>", self.restart)
        self.parent.parent.bind("<Control-r>", self.restart_rotate)
        self.restart_label.bind("<Enter>", self.start_rotation)
        self.rotation_angle = 0
        self.rotation_running = False

        self.language_var = ctk.StringVar(value="english")
        self.language_var.trace_add('write', self.load_language)
        self.language_menu = ctk.CTkOptionMenu(
            self.container,
            variable=self.language_var,
            values=languages,
            cursor="sb_down_arrow"
        )
        self.language_menu.pack(side="left", padx=10, pady=10)

        self.additional_options_frame = CTkFrame(self.container)
        self.additional_options_frame.pack(side="right", padx=(10, 25), pady=10)
        self.populate_subtype_options()

        self.update_type_colors()

    def translate_types(self):
        self.restart_tooltip.update_tooltip_text(f"{self.parent.translations[8]}, Ctrl+R")

        self.time_type.configure(text=self.parent.translations[9])  # Time
        self.words_type.configure(text=self.parent.translations[10])  # Words
        if self.selected_type == 0:
            self.parent.stats_frame.word_mode.set(self.parent.translations[9])
        else:
            self.parent.stats_frame.word_mode.set(self.parent.translations[10])

    def on_type_click(self, widget):
        if self.timer_running or (widget == self.time_type and self.selected_type == 0) or (
                widget == self.words_type and self.selected_type == 1):
            return
        if widget == self.time_type:
            self.selected_type = 0
            self.parent.stats_frame.word_mode.set(self.parent.translations[9])  # Time
        elif widget == self.words_type:
            self.selected_type = 1
            self.parent.stats_frame.word_mode.set(self.parent.translations[10])  # Words

        self.populate_subtype_options()
        self.update_type_colors()

    def update_type_colors(self):
        if self.selected_type == 0:
            self.time_type.configure(
                font=('Arial', 15, 'bold'),
                text_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"][self.parent.parent.is_dark_mode])
            self.words_type.configure(
                font=('Arial', 15),
                text_color=ctk.ThemeManager.theme["CTkEntry"]["placeholder_text_color"][
                    self.parent.parent.is_dark_mode]
            )
        else:
            self.time_type.configure(
                font=('Arial', 15),
                text_color=ctk.ThemeManager.theme["CTkEntry"]["placeholder_text_color"][
                    self.parent.parent.is_dark_mode]
            )
            self.words_type.configure(
                font=('Arial', 15, 'bold'),
                text_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"][self.parent.parent.is_dark_mode]
            )

    def populate_subtype_options(self):
        for widget in self.additional_options_frame.winfo_children():
            widget.destroy()
        if self.selected_type == 0:
            labels = ["30", "60", "90", "120"]
            self.progress_label.configure(text=f"{labels[0]}s")
            self.round_time = int(labels[0])
            self.time_left = self.round_time
        else:
            labels = ["10", "20", "30", "40"]
            self.progress_label.configure(text=f"0/{labels[0]}")
            self.words_needed = int(labels[0])
        self.selected_subtype = 0

        selected_color = ctk.ThemeManager.theme["CTkLabel"]["text_color"][self.parent.parent.is_dark_mode]
        unselected_color = ctk.ThemeManager.theme["CTkEntry"]["placeholder_text_color"][self.parent.parent.is_dark_mode]

        for i, text in enumerate(labels):
            label = CTkLabel(
                self.additional_options_frame,
                text=text,
                font=('Arial', 15),
                text_color=selected_color if i == self.selected_subtype else unselected_color,
                cursor="hand2"
            )
            label.pack(side="left", padx=10)
            label.bind("<Button-1>", lambda e, lbl=label: self.on_subtype_click(lbl))
            ToolTip(label, text=f"Ctrl+{i+1}")
            self.parent.parent.bind(f"<Control-Key-{i+1}>", lambda e, lbl=label: self.on_subtype_click(lbl))

    def on_subtype_click(self, label):
        clicked_on = self.additional_options_frame.winfo_children().index(label)
        if self.selected_subtype == clicked_on or self.timer_running:
            return
        self.update_subtype_colors(clicked_on)

    def update_subtype_colors(self, clicked_on):
        selected_color = ctk.ThemeManager.theme["CTkLabel"]["text_color"][self.parent.parent.is_dark_mode]
        unselected_color = ctk.ThemeManager.theme["CTkEntry"]["placeholder_text_color"][self.parent.parent.is_dark_mode]

        for widget in self.additional_options_frame.winfo_children():
            label = self.additional_options_frame.winfo_children()[clicked_on]
            if widget.cget("text") == label.cget("text"):
                widget.configure(text_color=selected_color)
                self.selected_subtype = self.additional_options_frame.winfo_children().index(widget)
                if self.selected_type == 0:
                    self.progress_label.configure(text=f"{int(label.cget('text'))}s")
                    self.round_time = int(label.cget('text'))
                    self.time_left = self.round_time
                else:
                    self.progress_label.configure(text=f"0/{int(label.cget('text'))}")
                    self.words_needed = int(label.cget('text'))
            else:
                widget.configure(text_color=unselected_color)

    def update_restart_button(self):
        self.original_restart_image = load_svg_image(
            "res/retry.svg",
            (20, 20),
            ctk.ThemeManager.theme["CTkLabel"]["text_color"][self.parent.parent.is_dark_mode]
        )
        self.restart_image = img_to_ctk(self.original_restart_image, self.rotation_angle)
        self.restart_label.configure(image=self.restart_image)

    def load_language(self, *args):
        for widget in self.parent.words_conveyor.pack_slaves():
            widget.destroy()
        self.parent.words = get_language_list(self.language_var.get())
        random.shuffle(self.parent.words)
        self.parent.populate_words()
        self.parent.stats_frame.word_list.set(self.language_var.get().capitalize())
        self.parent.translations = get_translations(self.language_var.get())
        self.parent.translate_labels()

    def timer_mode(self):
        def running():
            if not self.timer_running:
                return

            if self.time_left > 0:
                self.time_left -= 1
                self.progress_label.configure(text=f"{self.time_left}s")
                if self.time_left != self.round_time - 1:
                    self.parent.update_stats()
                self.progress_label.after(1000, running)
            else:
                self.end_config()

        running()

    def word_mode(self):
        def running():
            if not self.timer_running:
                return

            if self.parent.current_word < self.words_needed:
                self.parent.update_stats()
                self.progress_label.after(1000, running)
                print("still here")

        running()

    def restart(self, event=None):
        self.timer_running = False
        self.parent.focus_set()

        self.parent.char_index = 0
        self.parent.char_in_word = 0
        self.parent.current_word = 0
        self.parent.animation_in_progress = False
        self.parent.last_word_shown = self.parent.batch_size
        random.shuffle(self.parent.words)

        self.time_left = self.round_time
        if self.selected_type == 0:
            self.progress_label.configure(text=f"{self.time_left}s")
        else:
            self.progress_label.configure(text=f"0/{self.words_needed}")

        self.parent.populate_words()
        self.parent.stats_frame.reset_stats()
        self.parent.show_placeholder()

        self.language_menu.configure(state='normal')
        self.parent.entry.configure(state='normal')

    def start_rotation(self, event=None):
        self.rotation_angle = 0

        def rotate_image():
            if self.rotation_angle < 360:
                self.rotation_angle += 15
                self.restart_image = img_to_ctk(self.original_restart_image, self.rotation_angle)
                self.restart_label.configure(image=self.restart_image)
                self.after(10, rotate_image)
            else:
                self.rotation_running = False

        if not self.rotation_running:
            self.rotation_running = True
            rotate_image()

    def restart_rotate(self, event):
        self.start_rotation()
        self.after(150, self.restart)

    def start_a_round(self):
        if self.timer_running:
            return
        self.parent.hide_placeholder()
        self.timer_running = True
        self.parent.start_time = time.time()

        if self.selected_type == 0:
            self.timer_mode()
        if self.selected_type == 1:
            self.word_mode()

    def start_config(self):
        self.language_menu.configure(state='disabled')
        self.parent.entry.configure(state='normal')

    def end_config(self):
        self.parent.entry.configure(state='disabled')
        self.parent.parent.show_chart()
