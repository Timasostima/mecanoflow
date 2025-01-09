import time

from customtkinter import CTkFrame, CTkLabel
from tkinter import Entry
import customtkinter as ctk

from src.utils.config import Colors
from src.utils.extracted_lists import get_language_list, get_translations
from src.ui.statistics_frame import StatsFrame
from src.ui.top_bar import TopBar


class TypingApp(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(
            parent,
            fg_color=ctk.ThemeManager.theme["CTkFrame"]["fg_color"][parent.is_dark_mode],
            corner_radius=0
        )
        self.parent = parent
        self.start_time = None
        self.char_index = 0
        self.char_in_word = 0
        self.current_word = 0
        self.font_size = 55
        self.animation_in_progress = False
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.topBar = TopBar(self)
        self.topBar.grid(row=0, column=0, sticky='nsew')
        self.words = get_language_list(self.topBar.language_var.get())
        self.translations = get_translations(self.topBar.language_var.get())

        self.middleFrame = CTkFrame(
            self,
            height=self.font_size,
            border_color=ctk.ThemeManager.theme["CTkFrame"]["top_fg_color"][self.parent.is_dark_mode],
            border_width=2,
            corner_radius=0
        )
        self.middleFrame.grid(row=1, column=0, sticky='nsew')
        self.middleFrame.bind('<Configure>', self.recalculate_offset)

        self.words_conveyor = CTkFrame(
            self.middleFrame,
            fg_color=ctk.ThemeManager.theme["CTkFrame"]["fg_color"][self.parent.is_dark_mode],
        )
        self.words_conveyor.place(relx=0.5, rely=0.5, anchor='sw')
        self.input_conveyor = CTkFrame(
            self.middleFrame,
            fg_color=ctk.ThemeManager.theme["CTkFrame"]["fg_color"][self.parent.is_dark_mode],
            width=0
        )
        self.input_conveyor.place(relx=0.5, rely=0.5, anchor='nw')

        self.stats_frame = StatsFrame(self)
        self.update_layout()
        self.bind('<Configure>', lambda event: self.update_layout())

        self.batch_size = 8
        self.last_word_shown = self.batch_size

        self.valid = self.register(self.validator)
        self.entry = Entry(
            self.middleFrame,
            font=('Arial', self.font_size - int(self.font_size / 4), 'bold'),
            fg=ctk.ThemeManager.theme["CTkLabel"]["text_color"][self.parent.is_dark_mode],
            bg=ctk.ThemeManager.theme["CTkFrame"]["fg_color"][self.parent.is_dark_mode],
            bd=0,
            borderwidth=0,
            insertbackground=ctk.ThemeManager.theme["CTkLabel"]["text_color"][self.parent.is_dark_mode],
            highlightthickness=0,
            validate='key',
            validatecommand=(self.valid, '%P'),
        )
        self.entry.place(relx=0.5, rely=0.5, anchor='nw', width=400, height=self.font_size + 10)
        self.entry.bind('<KeyRelease>', self.on_key_release)
        self.entry.bind('<FocusIn>', lambda event: self.topBar.start_a_round())

        self.show_placeholder()
        self.animate_conveyors(0.5, 1)

        self.topBar.load_language()

    def show_placeholder(self):
        self.entry.delete(0, 'end')
        self.entry.insert(0, self.translations[7]) # Start typing here...
        self.entry.config(
            fg=ctk.ThemeManager.theme["CTkEntry"]["placeholder_text_color"][self.parent.is_dark_mode],
            font=('Arial', int(self.font_size / 3), 'bold')
        )

    def hide_placeholder(self):
        self.entry.delete(0, 'end')
        self.entry.config(
            fg=ctk.ThemeManager.theme["CTkLabel"]["text_color"][self.parent.is_dark_mode],
            font=('Arial', self.font_size - int(self.font_size / 4), 'bold')
        )

    def translate_labels(self):
        self.stats_frame.wpm_text.configure(text=self.translations[1])
        self.stats_frame.wpm_tooltip.update_tooltip_text(self.translations[11])
        for i, stat_name in enumerate(self.translations[2:7], start=2):
            self.stats_frame.grid_slaves(row=i, column=0)[0].configure(text=stat_name)
        self.show_placeholder()

        self.topBar.translate_types()

    def update_layout(self):
        window_height = self.parent.winfo_height()
        if window_height < 700:
            self.stats_frame.grid(row=0, column=1, rowspan=2)
            self.grid_columnconfigure(0, weight=1)
        else:
            self.stats_frame.grid(row=2, column=0)
            self.grid_columnconfigure(0, weight=1)
            self.grid_columnconfigure(1, weight=0)

    def update_stats(self):
        typed_text = [label.cget('text') if isinstance(label, CTkLabel) else ' ' for label in
                      self.input_conveyor.pack_slaves()]
        typed_words = "".join(typed_text).split(" ")
        reference_text = [label.cget('text') for label in self.words_conveyor.pack_slaves()][:self.char_index]
        reference_words = "".join(reference_text).split(" ")

        correct_words = sum(1 for tw, rw in zip(typed_words, reference_words) if tw == rw)
        word_accuracy = (correct_words / len(("".join(typed_text)).split(" "))) * 100 if len(
            reference_text) > 0 else 100
        self.stats_frame.word_accuracy.set(f"{word_accuracy:.2f}%")

        correct_characters = 0
        total_characters = 0

        for i, word in enumerate(reference_words):
            for j, char in enumerate(word):
                if j < len(typed_words[i]) and typed_words[i][j] == char:
                    correct_characters += 1
                total_characters += 1

        char_accuracy = (correct_characters / total_characters) * 100 if total_characters != 0 else 100
        self.stats_frame.character_accuracy.set(f"{char_accuracy:.2f}%")

        # Incorrect words
        incorrect_words = len(reference_words) - correct_words
        self.stats_frame.incorrect_words.set(f"{max(incorrect_words, 0)}")

        # Calculate WPM
        elapsed_time = (time.time() - self.start_time) / 60  # elapsed time in minutes
        wpm = (correct_characters / 5) / elapsed_time if elapsed_time > 0 else 0
        self.stats_frame.wpm_value.set(f"{wpm:.2f}")

        self.parent.wpm_data.append(int(wpm))
        self.parent.acc_data.append(int(char_accuracy))
        self.parent.errors_data.append(1 if incorrect_words > self.parent.errors_data.count(1) else 0)

    def populate_words(self):
        for widget in self.words_conveyor.pack_slaves():
            widget.destroy()
        for widget in self.input_conveyor.pack_slaves():
            widget.destroy()

        self.words_conveyor.place(relx=0.5, rely=0.5, anchor='sw')
        self.input_conveyor.place(relx=0.5, rely=0.5, anchor='nw')

        for word in self.words[:self.batch_size]:
            for char in word:
                label = CTkLabel(self.words_conveyor, text=char, font=('Arial', self.font_size, 'bold'))
                label.pack(side="left")
            label = CTkLabel(self.words_conveyor, text=" ", font=('Arial', self.font_size, 'bold'))
            label.pack(side="left")

    def add_word(self):
        if self.last_word_shown == self.current_word + self.batch_size - 1:
            if self.animation_in_progress:
                self.middleFrame.after(10, self.add_word)
            else:
                for char in self.words[self.current_word + self.batch_size - 1]:
                    label = CTkLabel(self.words_conveyor, text=char, font=('Arial', self.font_size, 'bold'))
                    label.pack(side="left")
                label = CTkLabel(self.words_conveyor, text=" ", font=('Arial', self.font_size, 'bold'))
                label.pack(side="left")
                self.last_word_shown += 1

    def validator(self, new_text):
        if not new_text:
            return True

        if new_text[-1] == " " and self.char_in_word == 0 and self.entry.index('end') == 0:
            return False

        if self.animation_in_progress:
            self.middleFrame.after(10, lambda: self.validator(new_text))
            return False
        if new_text[-1] == " ":
            self.handle_space()
            self.entry.config(validate='none')
            self.entry.delete(0, 'end')
            self.entry.config(validate='key')
            return False
        elif self.char_in_word == len(self.words[self.current_word]):
            return True
        elif new_text and new_text[0] == self.words[self.current_word][self.char_in_word]:
            CTkLabel(self.input_conveyor, text=new_text[0], font=('Arial', self.font_size, 'bold')).pack(side="left")
            self.handle_correct_char()
            return False
        return True

    def on_key_release(self, event):
        input_text = self.entry.get()

        # in case of continious correct chars (on erase)
        def process_input():
            nonlocal input_text
            if self.animation_in_progress:
                self.middleFrame.after(10, process_input)
            elif self.char_in_word == len(self.words[self.current_word]):
                return
            elif input_text and input_text[0] == self.words[self.current_word][self.char_in_word]:
                CTkLabel(self.input_conveyor, text=input_text[0], font=('Arial', self.font_size, 'bold')).pack(
                    side="left")
                self.entry.delete(0, 1)
                input_text = input_text[1:]
                self.handle_correct_char()
                self.middleFrame.after(10, process_input)

        process_input()
        self.add_word()

    def handle_space(self):
        self.animation_in_progress = True
        word_start = (
            ''.join([label.cget('text') for label in self.words_conveyor.pack_slaves()[:self.char_index]])
            .rindex(' ') + 1 if self.current_word > 0 else 0
        )
        word_end = (
            ''.join([label.cget('text') for label in self.words_conveyor.pack_slaves()[self.char_index:]])
            .index(' ') + self.char_index if self.current_word < len(self.words) else len(
                self.words_conveyor.pack_slaves())
        )

        if self.topBar.selected_type == 1:
            if self.current_word == self.topBar.words_needed:
                self.topBar.end_config()
            else:
                self.topBar.progress_label.configure(text=f"{self.current_word + 1}/{self.topBar.words_needed}")

        if self.char_in_word < len(self.words[self.current_word]):  # if it is not the whole word
            accumulative_width = sum(
                self.words_conveyor.pack_slaves()[self.char_index + character].winfo_width() for character in
                range(len(self.words[self.current_word]) + 1 - self.char_in_word))
            self.char_index += len(self.words[self.current_word]) + 1 - self.char_in_word
            spacer = CTkFrame(self.input_conveyor, width=accumulative_width, height=10)
            spacer.pack(side="left")
            for i in range(word_start, word_end):
                self.words_conveyor.pack_slaves()[i].configure(text_color=Colors.incorrect)
        else:  # if it is the whole word
            CTkLabel(self.input_conveyor, text=' ', font=('Arial', self.font_size, 'bold')).pack(side="left")
            accumulative_width = self.words_conveyor.pack_slaves()[self.char_index].winfo_width()
            self.char_index += 1
            for i in range(word_start, word_end):
                self.words_conveyor.pack_slaves()[i].configure(text_color=Colors.correct)

        new_relx = float(self.words_conveyor.place_info()['relx']) - (
                accumulative_width / self.middleFrame.winfo_width())
        self.animate_conveyors(new_relx, 20)
        self.current_word += 1
        self.char_in_word = 0

    def handle_correct_char(self):
        self.animation_in_progress = True
        char_width = self.words_conveyor.pack_slaves()[self.char_index].winfo_width()
        new_relx = float(self.words_conveyor.place_info()['relx']) - (char_width / self.middleFrame.winfo_width())
        self.animate_conveyors(new_relx, 5)
        self.char_index += 1
        self.char_in_word += 1

    def recalculate_offset(self, event):
        total_width = sum(self.words_conveyor.pack_slaves()[i].winfo_width() for i in range(self.char_index))
        new_relx = 0.5 - (total_width / self.middleFrame.winfo_width())
        self.words_conveyor.place_configure(relx=new_relx)
        self.input_conveyor.place_configure(relx=new_relx)

    def animate_conveyors(self, new_relx, steps):
        current_relx = float(self.words_conveyor.place_info()['relx'])
        step = (new_relx - current_relx) / steps

        def step_animation(steps_remaining):
            nonlocal current_relx
            if steps_remaining > 0:
                current_relx += step
                self.words_conveyor.place_configure(relx=current_relx)
                self.input_conveyor.place_configure(relx=current_relx)
                self.words_conveyor.after(5, step_animation, steps_remaining - 1)
            else:
                self.animation_in_progress = False

        step_animation(steps)
