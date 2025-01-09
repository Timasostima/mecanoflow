import customtkinter as ctk
from customtkinter import CTkFrame, CTkLabel

from src.utils.Images import load_image, img_to_ctk


class AppBar(CTkFrame):
    def __init__(self, parent):
        super().__init__(
            parent, corner_radius=0,
        )
        self.parent = parent

        # self.container = CTkFrame(
        #     self,
        #     corner_radius=0,
        #     fg_color=ctk.ThemeManager.theme["CTkFrame"]["fg_color"][self.parent.is_dark_mode]
        # )
        # self.container.pack()

        self.original_logo_image = load_image(
            "res/app_logo.png",
            ctk.ThemeManager.theme["CTkButton"]["fg_color"][self.parent.is_dark_mode]
        )
        self.logo_image = img_to_ctk(self.original_logo_image, size=(230, 50))
        self.logo_label = CTkLabel(
            self,
            image=self.logo_image,
            text=""
        )
        self.logo_label.pack(pady=(7, 5))

        # image = load_image(
        #     "res/change_theme_img.png",
        # )
        # image = img_to_ctk(image)
        # self.label = CTkLabel(
        #     self.container,
        #     image=image,
        #     text="",
        # )
        # self.label.pack(padx=50, side='right')
        # self.label.bind("<Button-1>", self.parent.change_color_theme)