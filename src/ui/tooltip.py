import customtkinter as ctk


class ToolTip:
    def __init__(self, widget, text, delay=1500):
        self.widget = widget
        self.text = text
        self.delay = delay
        self.tip_window = None
        self.id = None

        self.widget.bind("<Enter>", self.schedule_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def schedule_tooltip(self, event=None):
        self.id = self.widget.after(self.delay, self.show_tooltip)

    def show_tooltip(self, event=None):
        if self.tip_window is not None:
            return

        # Create a tooltip window
        self.tip_window = ctk.CTkToplevel(self.widget)
        self.tip_window.wm_overrideredirect(True)
        self.tip_window.wm_geometry(f"+{self.widget.winfo_rootx() + 20}+{self.widget.winfo_rooty() + 20}")

        # Tooltip content
        label = ctk.CTkLabel(
            self.tip_window, text=self.text,
            padx=5, pady=3,
            font=("Arial", 10)
        )
        label.pack()

    def hide_tooltip(self, event=None):
        if self.id:
            self.widget.after_cancel(self.id)
            self.id = None
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None

    def update_tooltip_text(self, new_text):
        self.text = new_text
        print("Tooltip text updated to:", new_text)