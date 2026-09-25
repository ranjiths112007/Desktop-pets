"""Ben 10 Desktop Pet — Pure Procedural Vector Engine.

Features:
- Pure Tkinter procedural vector art rendering (crisp, scalable, no image dependencies).
- Classic Ben 10 character with glowing Omnitrix wrist watch.
- Heatblast form with magma armor, head flames, chest Omnitrix badge, and flame particles.
- Eased multi-ring energy transformation sequence with radial energy beams.
- Borderless transparent floating desktop window with mouse dragging.
- Space / Double-Click to transform, P to pause walking, Right-Click / Escape to exit.
"""

from __future__ import annotations

import math
import random
import sys
import tkinter as tk
from dataclasses import dataclass

W, H, FPS = 330, 390, 33
BG = "#010101"
GREEN = "#B7FF00"
BLACK = "#151515"
SKIN = "#F1B27E"
HAIR = "#5C2F16"
FIRE = "#FF7A00"
YELLOW = "#FFF36A"
RED = "#7D220E"


@dataclass
class Particle:
    x: float
    y: float
    vx: float
    vy: float
    life: int
    size: float
    color: str


class Ben10Pet:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("Ben 10 Desktop Pet")
        root.overrideredirect(True)
        root.attributes("-topmost", True)
        root.configure(bg=BG)
        try:
            root.attributes("-transparentcolor", BG)
        except tk.TclError:
            pass

        self.c = tk.Canvas(root, width=W, height=H, bg=BG, highlightthickness=0)
        self.c.pack(fill="both", expand=True)

        self.root.update_idletasks()
        self.sw = root.winfo_screenwidth()
        self.sh = root.winfo_screenheight()

        self.x = max(20, (self.sw - W) // 2)
        self.y = max(20, (self.sh - H) // 2)
        self.dx = 1.2
        self.frame = 0
        self.state = "ben"
        self.tframe = 0
        self.paused = False
        self.drag = None
        self.particles_list = []

        self.c.bind("<ButtonPress-1>", self.start_drag)
        self.c.bind("<B1-Motion>", self.drag_window)
        self.c.bind("<ButtonRelease-1>", lambda e: setattr(self, "drag", None))
        self.c.bind("<Double-Button-1>", lambda e: self.toggle())
        self.c.bind("<Button-3>", lambda e: root.destroy())
        root.bind("<space>", lambda e: self.toggle())
        root.bind("<p>", lambda e: self.pause())
        root.bind("<Escape>", lambda e: root.destroy())

        self.root.geometry(f"{W}x{H}+{int(self.x)}+{int(self.y)}")
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()

        self.tick()

    def pause(self):
        self.paused = not self.paused

    def start_drag(self, e):
        self.drag = (e.x_root - self.x, e.y_root - self.y)

    def drag_window(self, e):
        if self.drag:
            self.x = max(0, e.x_root - self.drag[0])
            self.y = max(0, e.y_root - self.drag[1])
            self.root.geometry(f"+{int(self.x)}+{int(self.y)}")

    def toggle(self):
        if self.state in ("transforming", "returning"):
            return
        self.state = "transforming" if self.state == "ben" else "returning"
        self.tframe = 0
        self.particles_list = []

    def shape(self, kind, pts, fill, outline="", width=1):
        vals = [v for p in pts for v in p]
        getattr(self.c, kind)(*vals, fill=fill, outline=outline, width=width)

    def oval(self, box, fill="", outline="", width=1):
        self.c.create_oval(*box, fill=fill, outline=outline, width=width)

    def line(self, pts, fill, width):
        self.shape("create_line", pts, fill, width=width)

    def omnitrix(self, x, y, active=False):
        if active:
            for r in (25, 31, 37):
                self.oval((x - r, y - r, x + r, y + r), "", GREEN, 2)
        self.oval((x - 18, y - 12, x + 18, y + 12), "#3C3C3C", BLACK, 2)
        self.oval((x - 10, y - 10, x + 10, y + 10), "#BDBDBD", BLACK, 2)
        self.oval((x - 8, y - 8, x + 8, y + 8), GREEN if active else "#4E7B22", BLACK, 2)
        self.shape("create_polygon", [(x, y - 6), (x + 6, y), (x, y + 6), (x - 6, y)], "#F2FFF0", BLACK)

    def ben(self, bob=0):
        x, y = 165, 170 + bob
        self.oval((x - 62, 342, x + 62, 356), "#161616")
        self.line([(x - 18, y + 92), (x - 36, y + 166)], "#252525", 23)
        self.line([(x + 18, y + 92), (x + 38, y + 166)], "#252525", 23)
        self.line([(x - 42, y + 166), (x - 18, y + 166)], "#FFFFFF", 11)
        self.line([(x + 18, y + 166), (x + 46, y + 166)], "#FFFFFF", 11)
        self.shape("create_polygon", [(x - 38, y - 40), (x + 38, y - 40), (x + 47, y + 65), (x - 47, y + 65)], "#F2F2F2", BLACK, 3)
        self.shape("create_polygon", [(x - 38, y - 40), (x + 38, y - 40), (x + 31, y + 12), (x - 31, y + 12)], BLACK)
        self.line([(x - 35, y - 25), (x - 84, y + 18)], SKIN, 18)
        self.line([(x + 35, y - 25), (x + 84, y + 18)], SKIN, 18)
        self.oval((x - 96, y + 9, x - 73, y + 31), SKIN, BLACK, 2)
        self.oval((x + 73, y + 9, x + 96, y + 31), SKIN, BLACK, 2)
        self.oval((x - 34, y - 112, x + 34, y - 43), SKIN, BLACK, 3)
        self.shape(
            "create_polygon",
            [
                (x - 36, y - 86),
                (x - 40, y - 115),
                (x - 18, y - 130),
                (x - 2, y - 118),
                (x + 14, y - 131),
                (x + 39, y - 111),
                (x + 35, y - 81),
                (x + 13, y - 95),
                (x - 5, y - 82),
                (x - 18, y - 98),
            ],
            HAIR,
            BLACK,
            2,
        )
        self.oval((x - 21, y - 85, x - 10, y - 73), "#A6D62A", BLACK, 2)
        self.oval((x + 10, y - 85, x + 21, y - 73), "#A6D62A", BLACK, 2)
        self.oval((x - 17, y - 82, x - 13, y - 77), BLACK)
        self.oval((x + 13, y - 82, x + 17, y - 77), BLACK)
        self.line([(x - 13, y - 62), (x, y - 57), (x + 13, y - 62)], BLACK, 2)
        self.omnitrix(x - 76, y + 17, active=(self.state in ("transforming", "returning")))

    def flame(self, x, y, s):
        sway = math.sin(self.frame * 0.35 + x) * 5
        self.shape(
            "create_polygon",
            [
                (x, y + s),
                (x - s * 0.55, y + s * 0.2),
                (x - s * 0.35 + sway, y - s),
                (x + sway, y - s * 0.35),
                (x + s * 0.4, y - s * 0.85),
                (x + s * 0.55, y + s * 0.2),
            ],
            FIRE,
            YELLOW,
            2,
        )
        self.shape(
            "create_polygon",
            [
                (x, y + s * 0.5),
                (x - s * 0.22, y - s * 0.1),
                (x + sway * 0.3, y - s * 0.6),
                (x + s * 0.28, y - s * 0.05),
            ],
            YELLOW,
        )

    def heatblast(self, bob=0):
        x, y = 165, 180 + bob
        pulse = 4 + math.sin(self.frame * 0.25) * 4
        for r in (90 + pulse, 96 + pulse, 102 + pulse):
            self.oval((x - r, y + 15 - r, x + r, y + 15 + r), "", FIRE, 2)
        self.shape(
            "create_polygon",
            [
                (x - 38, y - 70),
                (x - 63, y - 119),
                (x - 25, y - 103),
                (x - 4, y - 151),
                (x + 10, y - 105),
                (x + 46, y - 125),
                (x + 34, y - 70),
            ],
            FIRE,
            YELLOW,
            3,
        )
        self.oval((x - 36, y - 92, x + 36, y - 26), RED, BLACK, 3)
        self.shape("create_polygon", [(x - 24, y - 72), (x + 24, y - 72), (x + 15, y - 40), (x - 15, y - 40)], "#4C1C10", YELLOW, 2)
        self.shape("create_polygon", [(x - 20, y - 67), (x - 3, y - 59), (x - 20, y - 52)], YELLOW, BLACK)
        self.shape("create_polygon", [(x + 20, y - 67), (x + 3, y - 59), (x + 20, y - 52)], YELLOW, BLACK)
        self.shape("create_polygon", [(x - 35, y - 35), (x + 35, y - 35), (x + 44, y + 76), (x - 44, y + 76)], RED, YELLOW, 3)
        self.line([(x - 30, y - 20), (x - 90, y + 28)], RED, 23)
        self.line([(x + 30, y - 20), (x + 90, y + 28)], RED, 23)
        self.flame(x - 98, y + 32, 28)
        self.flame(x + 98, y + 32, 28)
        self.line([(x - 18, y + 72), (x - 36, y + 157)], RED, 25)
        self.line([(x + 18, y + 72), (x + 40, y + 157)], RED, 25)
        self.flame(x - 39, y + 164, 23)
        self.flame(x + 43, y + 164, 23)
        self.oval((x - 15, y - 4, x + 15, y + 26), "#3B1B12", YELLOW, 2)
        self.shape("create_polygon", [(x, y + 1), (x + 8, y + 11), (x, y + 21), (x - 8, y + 11)], GREEN, BLACK)

    def spawn_particles(self, fire=False, count=5):
        palette = [FIRE, "#FFB000", YELLOW, "#FFFFFF"] if fire else [GREEN, "#EFFFF0", "#D7FF75", "#FFFFFF"]
        for _ in range(count):
            a, s = random.random() * math.tau, random.uniform(1.5, 5.5)
            self.particles_list.append(
                [
                    165 + random.uniform(-55, 55),
                    190 + random.uniform(-75, 75),
                    math.cos(a) * s,
                    math.sin(a) * s,
                    random.randint(15, 34),
                    random.uniform(2, 6),
                    random.choice(palette),
                ]
            )

    def update_particles(self):
        alive = []
        for p in self.particles_list:
            p[0] += p[2]
            p[1] += p[3]
            p[3] -= 0.04
            p[4] -= 1
            p[5] *= 0.97
            if p[4] > 0 and p[5] > 0.6:
                self.oval((p[0] - p[5], p[1] - p[5], p[0] + p[5], p[1] + p[5]), p[6])
                alive.append(p)
        self.particles_list = alive

    def transition(self, progress, to_heat):
        ease = progress * progress * (3 - 2 * progress)
        color = GREEN if to_heat else "#FFB000"
        radius = 28 + ease * 155
        for ring in range(4):
            r = radius - ring * 18
            if r > 4:
                self.oval((165 - r, 190 - r, 165 + r, 190 + r), "", color, max(1, 5 - ring))
        for angle in range(0, 360, 30):
            a = math.radians(angle + self.frame * 5)
            self.line(
                [
                    (165 + math.cos(a) * 42, 190 + math.sin(a) * 42),
                    (165 + math.cos(a) * (radius + 25), 190 + math.sin(a) * (radius + 25)),
                ],
                color,
                2,
            )
        self.spawn_particles(fire=not to_heat, count=6)
        if progress > 0.78:
            r = 40 + ((progress - 0.78) / 0.22) * 170
            self.oval((165 - r, 190 - r, 165 + r, 190 + r), "", "#FFFFFF" if to_heat else YELLOW, 5)

    def tick(self):
        self.frame += 1
        self.c.delete("all")
        bob = math.sin(self.frame * 0.12) * 3
        if self.state == "ben":
            self.ben(bob)
        elif self.state == "heatblast":
            self.heatblast(bob)
            self.spawn_particles(True, 1)
        else:
            progress = min(1.0, self.tframe / 42.0)
            to_heat = self.state == "transforming"
            if progress < 0.55:
                self.ben(bob) if to_heat else self.heatblast(bob)
            else:
                self.heatblast(bob) if to_heat else self.ben(bob)
            self.transition(progress, to_heat)
            self.tframe += 1
            if self.tframe >= 42:
                self.state = "heatblast" if to_heat else "ben"
                self.tframe = 0
        self.update_particles()
        self.c.create_text(
            8,
            10,
            anchor="nw",
            text="SPACE: transform | P: pause | Right-click: exit",
            fill=GREEN,
            font=("Segoe UI", 8, "bold"),
        )
        if not self.paused and self.state not in ("transforming", "returning"):
            self.x += self.dx * (0.7 if self.state == "heatblast" else 1.0)
            if self.x <= 0 or self.x >= self.sw - W:
                self.dx *= -1
        self.root.geometry(f"+{int(self.x)}+{int(self.y)}")
        self.root.after(FPS, self.tick)


def main():
    root = tk.Tk()
    Ben10Pet(root)
    root.mainloop()


if __name__ == "__main__":
    main()
