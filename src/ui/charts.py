import customtkinter as ctk
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import MaxNLocator

from scipy.interpolate import make_interp_spline  # For smoothing

from src.utils.Images import resolve_customtkinter_color

# translations = {
#     "en": {
#         "wpm_label": "WPM", #1
#         "accuracy_label": "Accuracy", #12
#         "errors_label": "Errors", #13
#         "time_label": "Time (s)", #14
#         "percentage_label": "Value" #15
#     },
# }


class ChartFrame(ctk.CTkFrame):
    def __init__(self, parent, data_wpm, data_acc, data_errors, is_dark_mode, translations): # 11+
        super().__init__(parent, corner_radius=0)
        self.parent = parent

        placeholder_color = ctk.ThemeManager.theme["CTkEntry"]["placeholder_text_color"][is_dark_mode]
        if not placeholder_color.startswith("#"):
            placeholder_color = resolve_customtkinter_color(placeholder_color)
        label_color = ctk.ThemeManager.theme["CTkLabel"]["text_color"][is_dark_mode]
        if not label_color.startswith("#"):
            label_color = resolve_customtkinter_color(label_color)
        frame_color = ctk.ThemeManager.theme["CTkFrame"]["fg_color"][is_dark_mode]
        if not frame_color.startswith("#"):
            frame_color = resolve_customtkinter_color(frame_color)
        top_frame_color = ctk.ThemeManager.theme["CTkFrame"]["top_fg_color"][is_dark_mode]
        if not top_frame_color.startswith("#"):
            top_frame_color = resolve_customtkinter_color(top_frame_color)

        self.configure(fg_color=top_frame_color)  # Background color
        self.figure = Figure(figsize=(5, 3), dpi=100, facecolor=frame_color)
        self.subplot = self.figure.add_subplot(111)

        # Smooth the data using spline interpolation
        x = np.arange(len(data_wpm))
        x_smooth = np.linspace(x.min(), x.max(), 300)

        # Smoothing WPM
        spline_wpm = make_interp_spline(x, data_wpm, k=2)
        wpm_smooth = spline_wpm(x_smooth)

        # Smoothing Accuracy
        spline_acc = make_interp_spline(x, data_acc, k=2)
        acc_smooth = spline_acc(x_smooth)

        # Plot the gray Accuracy line and fill area
        self.subplot.plot(
            x_smooth, acc_smooth,
            color=placeholder_color,
            linewidth=2,
            label=translations[12]
        )
        self.subplot.fill_between(x_smooth, acc_smooth, color=placeholder_color, alpha=0.2)

        # WPM line and fill area
        self.subplot.plot(
            x_smooth, wpm_smooth,
            color=ctk.ThemeManager.theme["CTkButton"]["fg_color"][is_dark_mode],
            linewidth=2,
            label=translations[1]
        )
        self.subplot.fill_between(
            x_smooth, wpm_smooth,
            color=ctk.ThemeManager.theme["CTkButton"]["fg_color"][is_dark_mode],
            alpha=0.2
        )  # Semi-transparent fill

        # Plot the red errors
        for i, error in enumerate(data_errors):
            if error:
                self.subplot.plot(x[i], data_wpm[i], 'ro', markersize=6)  # Red markers for errors

        # Chart styling
        self.subplot.set_facecolor(frame_color)  # Chart background
        self.subplot.spines['top'].set_color(label_color)
        self.subplot.spines['bottom'].set_color(label_color)
        self.subplot.spines['left'].set_color(label_color)
        self.subplot.spines['right'].set_color(label_color)
        self.subplot.tick_params(axis='x', colors=label_color, labelsize=8)
        self.subplot.tick_params(axis='y', colors=label_color, labelsize=8)

        # Set axis limits to remove padding
        self.subplot.set_xlim(x.min(), x.max())  # Remove padding on the x-axis
        self.subplot.set_ylim(
            min(min(data_wpm), min(data_acc)),  # -10
            max(max(data_wpm), max(data_acc))  # +10
        )  # Remove padding on y-axis

        # Axis labels
        # Set custom ticks (e.g., for time on x-axis)
        self.subplot.xaxis.set_major_locator(
            MaxNLocator(integer=True, prune='both', nbins=6))  # Limita la cantidad de ticks
        self.subplot.set_xlabel(translations[14], color=label_color, fontsize=6, labelpad=2)  # Time
        self.subplot.set_ylabel(translations[15], color=label_color, fontsize=6, labelpad=2)  # Value

        # Set custom ticks
        # self.subplot.set_xticks(range(0, len(data_wpm)))

        tick_spacing = max(1, len(data_wpm) // 10)  # Mostrar aproximadamente 10 ticks espaciados
        selected_ticks = np.arange(0, len(data_wpm), tick_spacing)
        self.subplot.set_xticks(selected_ticks)
        self.subplot.set_xticklabels([str(i + 1) for i in selected_ticks], color=label_color, fontsize=8)

        # self.subplot.set_xticklabels([str(i) for i in range(1, len(data_wpm) + 1)], color=label_color, fontsize=8)
        self.subplot.yaxis.set_tick_params(labelsize=8)
        ytks = range(
            # int(min(min(data_wpm), min(data_acc))) - 10,
            int(min(min(data_wpm), min(data_acc))),
            # int(max(max(data_wpm), max(data_acc))) + 20,
            int(max(max(data_wpm), max(data_acc))),
            10
        )
        self.subplot.set_yticks(ytks)
        self.subplot.set_yticklabels([str(i) for i in ytks], color=label_color, fontsize=8)

        self.subplot.legend(
            loc="upper left",
            facecolor=top_frame_color,
            edgecolor=label_color,
            fontsize=8,
        )  # Add legend


        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill="both", expand=True)

        # Ensure the canvas renders correctly on launch
        self.canvas.draw()


if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("600x400")

    wpm_data = [60, 45, 50, 40, 55, 65, 50, 45, 55, 60]
    acc_data = [80, 75, 77, 78, 81, 85, 83, 79, 82, 84]
    errors_data = [0, 1, 0, 0, 1, 0, 1, 0, 1, 0]

    chart_frame = ChartFrame(app, wpm_data, acc_data, errors_data)
    chart_frame.pack(fill="both", expand=True, padx=10, pady=10)

    app.mainloop()
