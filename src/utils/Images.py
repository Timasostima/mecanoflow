from customtkinter import CTkImage

from PIL import Image
import cairosvg
import io


def img_to_ctk(img: Image, rotation=0, size=None):
    rotated = img.rotate(rotation)
    if size:
        return CTkImage(light_image=rotated, size=size)
    else:
        return CTkImage(light_image=rotated)


def resolve_customtkinter_color(color_name: str):
    if color_name.startswith("gray"):
        grey_value = int(color_name[4:])
        if 0 <= grey_value <= 100:
            print("here2")
            intensity = int((grey_value / 100) * 255)
            return f"#{intensity:02X}{intensity:02X}{intensity:02X}"
    # else: # for if
    #     return "#000000"


def hex_to_rgb(hex_color: str) -> tuple:
    if not hex_color.startswith("#"):
        hex_color = resolve_customtkinter_color(hex_color)

    hex_color = hex_color.lstrip('#')
    if len(hex_color) != 6 or not all(c in '0123456789abcdefABCDEF' for c in hex_color):
        raise ValueError(f"Invalid hex color format: {hex_color}")

    # Convert to RGB tuple
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))


def replace_colors_in_image(img: Image, color_hex: str):
    color_rgb = hex_to_rgb(color_hex)
    print(f"Color '{color_hex}' converted to RGB {color_rgb}.")

    img = img.convert("RGBA")
    pixels = img.load()

    for y in range(img.height):
        for x in range(img.width):
            # if pixels[x, y][3] != 0:  # Check if pixel is not transparent
            pixels[x, y] = (*color_rgb, pixels[x, y][3])

    return img


def load_svg_image(file_path, size, color_replace=None):
    png_data = cairosvg.svg2png(url=file_path, output_width=size[0], output_height=size[1])
    img = Image.open(io.BytesIO(png_data))

    if color_replace:
        img = replace_colors_in_image(img, color_replace)

    return img


def load_image(file_path, color_replace=None):
    img = Image.open(file_path)
    if color_replace:
        img = replace_colors_in_image(img, color_replace)

    return img
