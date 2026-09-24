"""Ben 10 desktop pet prototype.

Run:
    pip install -r requirements.txt
    python ben10_pet.py

Put your personal image files in assets/:
    assets/ben10.jpg
    assets/heatblast.png

The loader removes near-white backgrounds and uses the supplied images when
available. If they are missing, it falls back to simple vector art.
"""

from __future__ import annotations

import math
import random
import tkinter as tk
from pathlib import Path

try:
    from PIL import Image, ImageEnhance, ImageTk
except ImportError:  # graceful fallback: vector mode still works
    Image = ImageEnhance = ImageTk = None

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"
BEN_IMAGE = ASSETS_DIR / "ben10.jpg"
HEATBLAST_IMAGE = ASSETS_DIR / "heatblast.png"

WINDOW_W = 280
WINDOW_H = 330
TRANSPARENT = "#010101"
GREEN = "#b7ff00"


class Ben10Pet:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Ben 10 Desktop Pet")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.configure(bg=TRANSPARENT)
        try:
            self.root.attributes("-transparentcolor", TRANSPARENT)
        except tk.TclError:
            pass

        self.canvas = tk.Canvas(
            root,
            width=WINDOW_W,
            height=WINDOW_H,
            bg=TRANSPARENT,
            highlightthickness=0,
        )
        self.canvas.pack()

        self.screen_w = root.winfo_screenwidth()
        self.screen_h = root.winfo_screenheight()
        self.pos_x = 80
        self.pos_y = max(60, self.screen_h - WINDOW_H - 80)
        self.velocity = 2
        self.frame = 0
        self.transform_frame = 0
        self.state = "ben"
        self.drag_offset = None
        self.current_photo = None
        self.ben_photo = self.load_character(BEN_IMAGE, crop_right=True)
        self.heatblast_photo = self.load_character(HEATBLAST_IMAGE)

        self.canvas.bind("<ButtonPress-1>", self.start_drag)
        self.canvas.bind("<B1-Motion>", self.drag_window)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drag)
        self.canvas.bind("<Double-Button-1>", lambda _event: self.transform())
        self.canvas.bind("<Button-3>", lambda _event: self.root.destroy())
        self.root.bind("<space>", lambda _event: self.transform())
        self.root.bind("<Escape>", lambda _event: self.root.destroy())
        self.root.focus_force()
        self.root.geometry(f"{WINDOW_W}x{WINDOW_H}+{self.pos_x}+{self.pos_y}")
        self.tick()

    def load_character(self, path: Path, crop_right: bool = False):
        if Image is None or not path.exists():
            return None
        try:
            image = Image.open(path).convert("RGBA")
            if crop_right:
                # The provided Ben image contains a logo on the left and Ben
                # on the right. Keep the right-hand character area.
                image = image.crop((image.width // 2, 0, image.width, image.height))

            pixels = image.load()
            for y in range(image.height):
                for x in range(image.width):
                    r, g, b, a = pixels[x, y]
                    if r > 242 and g > 242 and b > 242:
                        pixels[x, y] = (255, 255, 255, 0)

            image.thumbnail((230, 285), Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(image)
        except Exception as exc:
            print(f"Could not load {path.name}: {exc}")
            return None

    def start_drag(self, event):
        self.drag_offset = (event.x_root - self.pos_x, event.y_root - self.pos_y)

    def drag_window(self, event):
        if self.drag_offset is None:
            return
        self.pos_x = max(0, event.x_root - self.drag_offset[0])
        self.pos_y = max(0, event.y_root - self.drag_offset[1])
        self.root.geometry(f"+{self.pos_x}+{self.pos_y}")

    def stop_drag(self, _event):
        self.drag_offset = None

    def transform(self):
        if self.state in {"transform", "heatblast"}:
            return
        self.state = "transform"
        self.transform_frame = 0

    def draw_omnitrix(self, x: int, y: int, glow: bool = False):
        ring = GREEN if glow else "#8bff00"
        fill = "#caff42" if glow else "#252525"
        self.canvas.create_oval(x - 17, y - 11, x + 17, y + 11, fill=fill, outline=ring, width=3)
        self.canvas.create_oval(x - 7, y - 7, x + 7, y + 7, fill="#111111", outline="#eaffb0")
        self.canvas.create_polygon(x, y - 5, x + 5, y, x, y + 5, x - 5, y, fill=GREEN)

    def draw_vector_ben(self):
        x, y = 140, 160
        self.canvas.create_oval(x - 28, y - 100, x + 28, y - 44, fill="#e8aa78", outline="#222222", width=2)
        self.canvas.create_arc(x - 30, y - 108, x + 30, y - 42, start=0, extent=180, fill="#5b2d13", outline="#5b2d13")
        self.canvas.create_rectangle(x - 32, y - 44, x + 32, y + 38, fill="#eeeeee", outline="#222222", width=2)
        self.canvas.create_rectangle(x - 32, y - 44, x + 32, y - 5, fill="#252525", outline="#252525")
        self.canvas.create_line(x - 30, y - 25, x - 74, y + 12, fill="#e8aa78", width=15)
        self.canvas.create_line(x + 30, y - 25, x + 74, y + 12, fill="#e8aa78", width=15)
        self.draw_omnitrix(x - 72, y + 8)
        self.canvas.create_line(x - 15, y + 38, x - 28, y + 105, fill="#252525", width=17)
        self.canvas.create_line(x + 15, y + 38, x + 28, y + 105, fill="#252525", width=17)
        self.canvas.create_line(x - 38, y + 107, x - 15, y + 107, fill="#eeeeee", width=9)
        self.canvas.create_line(x + 15, y + 107, x + 38, y + 107, fill="#eeeeee", width=9)

    def draw_vector_heatblast(self):
        x, y = 140, 160
        pulse = 10 + int(5 * math.sin(self.transform_frame / 2))
        self.canvas.create_oval(x - 70 - pulse, y - 125 - pulse, x + 70 + pulse, y + 130 + pulse, outline=GREEN, width=3)
        self.canvas.create_polygon(
            x - 42, y - 38, x - 65, y - 104, x - 20, y - 78,
            x, y - 145, x + 20, y - 78, x + 65, y - 104,
            x + 42, y - 38, fill="#ff8c00", outline="#ffe45e",
        )
        self.canvas.create_oval(x - 34, y - 75, x + 34, y - 8, fill="#ffb52e", outline="#ffe45e", width=2)
        self.canvas.create_rectangle(x - 38, y - 8, x + 38, y + 78, fill="#a92b09", outline="#ffe45e", width=2)
        self.canvas.create_line(x - 38, y, x - 85, y + 45, fill="#ffb52e", width=18)
        self.canvas.create_line(x + 38, y, x + 85, y + 45, fill="#ffb52e", width=18)
        self.canvas.create_line(x - 18, y + 78, x - 35, y + 145, fill="#a92b09", width=19)
        self.canvas.create_line(x + 18, y + 78, x + 35, y + 145, fill="#a92b09", width=19)

    def draw_character(self, photo, fallback):
        if photo is not None:
            self.current_photo = photo
            self.canvas.create_image(WINDOW_W // 2, 165, image=photo)
        else:
            fallback()

    def draw_transform_effect(self):
        intensity = min(120, 20 + self.transform_frame * 5)
        self.canvas.create_oval(
            140 - intensity, 160 - intensity,
            140 + intensity, 160 + intensity,
            outline=GREEN, width=4,
        )
        for angle in range(0, 360, 45):
            radians = math.radians(angle + self.transform_frame * 10)
            x1 = 140 + math.cos(radians) * 45
            y1 = 160 + math.sin(radians) * 45
            x2 = 140 + math.cos(radians) * 110
            y2 = 160 + math.sin(radians) * 110
            self.canvas.create_line(x1, y1, x2, y2, fill=GREEN, width=3)

    def tick(self):
        self.canvas.delete("all")
        self.frame += 1

        if self.state == "ben":
            self.draw_character(self.ben_photo, self.draw_vector_ben)
            self.draw_omnitrix(68, 173)
            self.pos_x += self.velocity
            if self.pos_x <= 0 or self.pos_x >= self.screen_w - WINDOW_W:
                self.velocity *= -1

        elif self.state == "transform":
            self.transform_frame += 1
            self.draw_character(self.ben_photo, self.draw_vector_ben)
            self.draw_omnitrix(68, 173, glow=True)
            self.draw_transform_effect()
            if self.transform_frame >= 24:
                self.state = "heatblast"
                self.transform_frame = 0

        elif self.state == "heatblast":
            self.transform_frame += 1
            self.draw_character(self.heatblast_photo, self.draw_vector_heatblast)
            self.draw_transform_effect()
            if self.transform_frame >= 180:
                self.state = "ben"
                self.transform_frame = 0

        self.canvas.create_text(
            8, 8,
            anchor="nw",
            text="Double-click / SPACE: transform  |  Right-click: exit",
            fill=GREEN,
            font=("Segoe UI", 8),
        )
        self.root.after(55, self.tick)


def main():
    root = tk.Tk()
    Ben10Pet(root)
    root.mainloop()


if __name__ == "__main__":
    main()
