"""Ben 10 Desktop Pet — Complete Master Build Engine.

Features:
- Borderless, always-on-top, transparent desktop pet window.
- Custom user image assets for Ben 10, Heatblast, and Green Energy Portal Ring.
- State-machine driven animation: Ben 10 & Heatblast forms.
- Natural desktop movement, edge detection, direction flipping, idle bobbing, and hopping.
- Layered Omnitrix activation & energy portal transformation timeline.
- High-performance particle engine (green energy sparks, flame embers, radial beams, rings).
- Mouse dragging, double-click transform, spacebar control, and right-click context menu.
- Preprocessed transparent PNG images with high quality fallback support.
"""

from __future__ import annotations

import math
import random
import sys
import tkinter as tk
from enum import Enum, auto
from pathlib import Path
from typing import List, Optional, Tuple

try:
    from PIL import Image, ImageEnhance, ImageTk
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

# Paths & Directories
BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"
BEN_IMAGE_PATH = ASSETS_DIR / "ben10.png"
HEATBLAST_IMAGE_PATH = ASSETS_DIR / "heatblast.png"
ENERGY_RING_PATH = ASSETS_DIR / "energy_ring.png"

# Constants & Settings
WINDOW_W = 280
WINDOW_H = 340
TRANSPARENT_COLOR = "#010101"
OMNITRIX_GREEN = "#b7ff00"
DARK_GREEN = "#3a7d00"
HEATBLAST_ORANGE = "#ff6a00"
HEATBLAST_RED = "#d93600"
HEATBLAST_YELLOW = "#ffdf38"
WHITE_HIGHLIGHT = "#ffffff"


class PetState(Enum):
    IDLE_BEN = auto()
    WALK_BEN = auto()
    ACTIVATE_OMNITRIX = auto()
    TRANSFORMING_TO_HEATBLAST = auto()
    IDLE_HEATBLAST = auto()
    WALK_HEATBLAST = auto()
    TRANSFORMING_TO_BEN = auto()
    PAUSED = auto()


class Particle:
    """Particle effect representation for energy rings, sparks, and embers."""

    def __init__(
        self,
        x: float,
        y: float,
        vx: float,
        vy: float,
        color: str,
        radius: float,
        life: int,
        p_type: str = "spark",
    ):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.radius = radius
        self.life = life
        self.max_life = life
        self.p_type = p_type

    def update(self) -> bool:
        self.x += self.vx
        self.y += self.vy
        self.life -= 1
        if self.p_type == "ember":
            self.radius = max(0.5, self.radius * 0.96)
            self.vy -= 0.05  # Buoyancy for embers
        elif self.p_type == "spark":
            self.vx *= 0.95
            self.vy *= 0.95
        elif self.p_type == "ring":
            self.radius += 3.5
        return self.life > 0


class Ben10PetEngine:
    """Main Application Engine for the Ben 10 Desktop Pet."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Ben 10 Desktop Pet")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.configure(bg=TRANSPARENT_COLOR)

        try:
            self.root.attributes("-transparentcolor", TRANSPARENT_COLOR)
        except tk.TclError:
            pass

        self.canvas = tk.Canvas(
            root,
            width=WINDOW_W,
            height=WINDOW_H,
            bg=TRANSPARENT_COLOR,
            highlightthickness=0,
        )
        self.canvas.pack(fill="both", expand=True)

        # Screen dimensions & positioning
        self.screen_w = root.winfo_screenwidth()
        self.screen_h = root.winfo_screenheight()
        self.pos_x = 100
        self.pos_y = max(50, self.screen_h - WINDOW_H - 90)
        self.velocity_x = 3.0
        self.direction = 1  # 1 = right, -1 = left

        # State management
        self.state = PetState.IDLE_BEN
        self.prev_state = PetState.IDLE_BEN
        self.frame = 0
        self.state_frame = 0
        self.state_timer = random.randint(120, 240)
        self.hop_frame = 0
        self.is_hopping = False
        self.drag_offset: Optional[Tuple[int, int]] = None
        self.high_quality_particles = True

        # Particle engine
        self.particles: List[Particle] = []

        # Asset loading
        self.ben_img_right, self.ben_img_left = self.load_character_images(BEN_IMAGE_PATH)
        self.heat_img_right, self.heat_img_left = self.load_character_images(HEATBLAST_IMAGE_PATH)
        self.ring_photos = self.load_ring_frames(ENERGY_RING_PATH)

        # Bindings
        self.canvas.bind("<ButtonPress-1>", self.start_drag)
        self.canvas.bind("<B1-Motion>", self.drag_window)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drag)
        self.canvas.bind("<Double-Button-1>", lambda _e: self.trigger_transformation())
        self.canvas.bind("<Button-3>", self.show_context_menu)
        self.root.bind("<space>", lambda _e: self.trigger_transformation())
        self.root.bind("<Escape>", lambda _e: self.root.destroy())

        # Setup context menu
        self.context_menu = tk.Menu(self.root, tearoff=0, bg="#1a1a1a", fg=OMNITRIX_GREEN, activebackground=DARK_GREEN)
        self.context_menu.add_command(label="⚡ Transform / Switch Form (Space)", command=self.trigger_transformation)
        self.context_menu.add_command(label="🦘 Hop / Jump", command=self.trigger_hop)
        self.context_menu.add_command(label="⏸️ Pause / Resume Walking", command=self.toggle_pause)
        self.context_menu.add_command(label="✨ Toggle Particle Quality", command=self.toggle_quality)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="❌ Exit Desktop Pet (Esc)", command=self.root.destroy)

        self.root.focus_force()
        self.root.geometry(f"{WINDOW_W}x{WINDOW_H}+{int(self.pos_x)}+{int(self.pos_y)}")

        # Start animation tick loop (~30 FPS)
        self.tick()

    def load_character_images(
        self, path: Path
    ) -> Tuple[Optional[ImageTk.PhotoImage], Optional[ImageTk.PhotoImage]]:
        """Load character image and pre-cache left/right facing photos."""
        if not HAS_PIL or not path.exists():
            return None, None
        try:
            image = Image.open(path).convert("RGBA")

            # Resize maintaining aspect ratio
            max_size = (210, 260)
            image.thumbnail(max_size, Image.Resampling.LANCZOS)

            img_right = ImageTk.PhotoImage(image)
            img_left = ImageTk.PhotoImage(image.transpose(Image.FLIP_LEFT_RIGHT))
            return img_right, img_left
        except Exception as exc:
            print(f"Could not load image {path.name}: {exc}")
            return None, None

    def load_ring_frames(self, path: Path) -> List[ImageTk.PhotoImage]:
        """Pre-cache scaled and rotated energy ring frames for portal animation."""
        if not HAS_PIL or not path.exists():
            return []
        try:
            base_ring = Image.open(path).convert("RGBA")
            base_ring = base_ring.resize((220, 220), Image.Resampling.LANCZOS)
            frames = []
            for angle in range(0, 360, 45):
                rotated = base_ring.rotate(angle, resample=Image.Resampling.BICUBIC)
                frames.append(ImageTk.PhotoImage(rotated))
            return frames
        except Exception as exc:
            print(f"Could not load energy ring: {exc}")
            return []

    # Dragging & Context Menu
    def start_drag(self, event):
        self.drag_offset = (event.x_root - self.pos_x, event.y_root - self.pos_y)

    def drag_window(self, event):
        if self.drag_offset:
            self.pos_x = event.x_root - self.drag_offset[0]
            self.pos_y = event.y_root - self.drag_offset[1]
            self.root.geometry(f"+{int(self.pos_x)}+{int(self.pos_y)}")

    def stop_drag(self, _event):
        self.drag_offset = None

    def show_context_menu(self, event):
        self.context_menu.tk_popup(event.x_root, event.y_root)

    # State Machine Controls
    def trigger_transformation(self):
        if self.state in (PetState.ACTIVATE_OMNITRIX, PetState.TRANSFORMING_TO_HEATBLAST, PetState.TRANSFORMING_TO_BEN):
            return

        if self.state in (PetState.IDLE_BEN, PetState.WALK_BEN, PetState.PAUSED) and self.prev_state != PetState.IDLE_HEATBLAST:
            self.state = PetState.ACTIVATE_OMNITRIX
            self.state_frame = 0
            self.spawn_omnitrix_burst()
        elif self.state in (PetState.IDLE_HEATBLAST, PetState.WALK_HEATBLAST) or (self.state == PetState.PAUSED and self.prev_state in (PetState.IDLE_HEATBLAST, PetState.WALK_HEATBLAST)):
            self.state = PetState.TRANSFORMING_TO_BEN
            self.state_frame = 0
            self.spawn_heatblast_reverse_burst()

    def trigger_hop(self):
        if not self.is_hopping:
            self.is_hopping = True
            self.hop_frame = 0

    def toggle_pause(self):
        if self.state == PetState.PAUSED:
            self.state = self.prev_state if self.prev_state != PetState.PAUSED else PetState.IDLE_BEN
        else:
            self.prev_state = self.state
            self.state = PetState.PAUSED

    def toggle_quality(self):
        self.high_quality_particles = not self.high_quality_particles

    # Particle Generators
    def spawn_omnitrix_burst(self):
        cx, cy = WINDOW_W // 2, 170
        count = 35 if self.high_quality_particles else 18
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2.0, 7.0)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            color = random.choice([OMNITRIX_GREEN, DARK_GREEN, WHITE_HIGHLIGHT, "#eaffb0"])
            self.particles.append(Particle(cx, cy, vx, vy, color, random.uniform(3, 6), random.randint(15, 30), "spark"))

    def spawn_transformation_ring(self, radius_start: float = 10.0):
        cx, cy = WINDOW_W // 2, 170
        self.particles.append(Particle(cx, cy, 0, 0, OMNITRIX_GREEN, radius_start, 18, "ring"))

    def spawn_heatblast_embers(self):
        cx = WINDOW_W // 2 + random.randint(-45, 45)
        cy = 230 + random.randint(-20, 20)
        vx = random.uniform(-1.0, 1.0)
        vy = random.uniform(-4.0, -1.5)
        color = random.choice([HEATBLAST_ORANGE, HEATBLAST_RED, HEATBLAST_YELLOW, "#ffffff"])
        self.particles.append(Particle(cx, cy, vx, vy, color, random.uniform(3, 7), random.randint(20, 45), "ember"))

    def spawn_heatblast_reverse_burst(self):
        cx, cy = WINDOW_W // 2, 170
        count = 40 if self.high_quality_particles else 20
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(3.0, 8.0)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            color = random.choice([HEATBLAST_ORANGE, OMNITRIX_GREEN, HEATBLAST_YELLOW, WHITE_HIGHLIGHT])
            self.particles.append(Particle(cx, cy, vx, vy, color, random.uniform(4, 7), random.randint(15, 30), "spark"))

    def update_particles(self):
        self.particles = [p for p in self.particles if p.update()]
        for p in self.particles:
            if p.p_type == "ring":
                self.canvas.create_oval(
                    p.x - p.radius, p.y - p.radius,
                    p.x + p.radius, p.y + p.radius,
                    outline=p.color, width=4
                )
            else:
                self.canvas.create_oval(
                    p.x - p.radius, p.y - p.radius,
                    p.x + p.radius, p.y + p.radius,
                    fill=p.color, outline=""
                )

    # Rendering Helpers
    def get_current_image(self, img_right: Optional[ImageTk.PhotoImage], img_left: Optional[ImageTk.PhotoImage]) -> Optional[ImageTk.PhotoImage]:
        return img_right if self.direction == 1 else img_left

    def draw_character(self, photo: Optional[ImageTk.PhotoImage], fallback_func):
        cx = WINDOW_W // 2
        cy = 170

        # Calculate vertical bob or hop offset
        y_offset = 0
        if self.is_hopping:
            self.hop_frame += 1
            y_offset = -abs(math.sin(self.hop_frame * 0.25)) * 30
            if self.hop_frame >= 12:
                self.is_hopping = False
                self.hop_frame = 0
        else:
            y_offset = math.sin(self.frame * 0.1) * 4  # Subtle breathing/idle bob

        if photo is not None:
            self.canvas.create_image(cx, cy + y_offset, image=photo)
        else:
            fallback_func(cx, cy + y_offset)

    def draw_energy_ring_overlay(self, cx: int, cy: int):
        """Draw animated rotating energy portal ring asset if available."""
        if self.ring_photos:
            frame_idx = (self.state_frame // 2) % len(self.ring_photos)
            self.canvas.create_image(cx, cy, image=self.ring_photos[frame_idx])

    def draw_omnitrix_wrist(self, x: int, y: int, glow: bool = False):
        color = OMNITRIX_GREEN if glow else "#252525"
        ring_color = WHITE_HIGHLIGHT if glow else OMNITRIX_GREEN
        pulse = int(3 * math.sin(self.frame * 0.3)) if glow else 0

        self.canvas.create_oval(x - 14 - pulse, y - 9 - pulse, x + 14 + pulse, y + 9 + pulse, fill=color, outline=ring_color, width=2)
        self.canvas.create_oval(x - 6, y - 6, x + 6, y + 6, fill="#111111", outline="#ffffff")
        self.canvas.create_polygon(x, y - 4, x + 4, y, x, y + 4, x - 4, y, fill=OMNITRIX_GREEN)

    # Vector Art Fallbacks
    def draw_vector_ben(self, cx: int, cy: int):
        self.canvas.create_oval(cx - 26, cy - 85, cx + 26, cy - 35, fill="#e8aa78", outline="#222222", width=2)
        self.canvas.create_arc(cx - 28, cy - 92, cx + 28, cy - 36, start=0, extent=180, fill="#5b2d13", outline="#5b2d13")
        self.canvas.create_rectangle(cx - 30, cy - 35, cx + 30, cy + 35, fill="#ffffff", outline="#222222", width=2)
        self.canvas.create_rectangle(cx - 10, cy - 35, cx + 10, cy + 35, fill="#252525", outline="#252525")
        self.canvas.create_line(cx - 28, cy - 20, cx - 60, cy + 15, fill="#e8aa78", width=13)
        self.canvas.create_line(cx + 28, cy - 20, cx + 60, cy + 15, fill="#e8aa78", width=13)
        self.draw_omnitrix_wrist(cx - 58, cy + 12)
        self.canvas.create_line(cx - 14, cy + 35, cx - 22, cy + 95, fill="#252525", width=15)
        self.canvas.create_line(cx + 14, cy + 35, cx + 22, cy + 95, fill="#252525", width=15)
        self.canvas.create_line(cx - 32, cy + 96, cx - 10, cy + 96, fill="#eeeeee", width=8)
        self.canvas.create_line(cx + 10, cy + 96, cx + 32, cy + 96, fill="#eeeeee", width=8)

    def draw_vector_heatblast(self, cx: int, cy: int):
        pulse = int(4 * math.sin(self.frame * 0.2))
        self.canvas.create_oval(cx - 60 - pulse, cy - 110 - pulse, cx + 60 + pulse, cy + 110 + pulse, fill="", outline=HEATBLAST_ORANGE, width=3)
        self.canvas.create_polygon(
            cx - 35, cy - 40, cx - 55, cy - 105, cx - 18, cy - 75,
            cx, cy - 135, cx + 18, cy - 75, cx + 55, cy - 105, cx + 35, cy - 40,
            fill=HEATBLAST_ORANGE, outline=HEATBLAST_YELLOW, width=2
        )
        self.canvas.create_oval(cx - 28, cy - 70, cx + 28, cy - 15, fill=HEATBLAST_YELLOW, outline="#8c1c00", width=2)
        self.canvas.create_rectangle(cx - 32, cy - 15, cx + 32, cy + 65, fill=HEATBLAST_RED, outline=HEATBLAST_YELLOW, width=2)
        self.canvas.create_line(cx - 32, cy - 5, cx - 70, cy + 40, fill=HEATBLAST_YELLOW, width=16)
        self.canvas.create_line(cx + 32, cy - 5, cx + 70, cy + 40, fill=HEATBLAST_YELLOW, width=16)
        self.canvas.create_line(cx - 16, cy + 65, cx - 28, cy + 125, fill=HEATBLAST_RED, width=17)
        self.canvas.create_line(cx + 16, cy + 65, cx + 28, cy + 125, fill=HEATBLAST_RED, width=17)

    # Main Animation & Movement Tick Loop
    def tick(self):
        self.canvas.delete("all")
        self.frame += 1

        # Desktop Movement Logic
        if self.state in (PetState.WALK_BEN, PetState.WALK_HEATBLAST):
            self.pos_x += self.velocity_x * self.direction
            if self.pos_x <= 10:
                self.pos_x = 10
                self.direction = 1
            elif self.pos_x >= self.screen_w - WINDOW_W - 10:
                self.pos_x = self.screen_w - WINDOW_W - 10
                self.direction = -1

            self.root.geometry(f"+{int(self.pos_x)}+{int(self.pos_y)}")

            # Random state switching between walking and idle
            self.state_timer -= 1
            if self.state_timer <= 0:
                self.state_timer = random.randint(120, 300)
                if self.state == PetState.WALK_BEN:
                    self.state = PetState.IDLE_BEN
                else:
                    self.state = PetState.IDLE_HEATBLAST

        elif self.state in (PetState.IDLE_BEN, PetState.IDLE_HEATBLAST):
            self.state_timer -= 1
            if self.state_timer <= 0:
                self.state_timer = random.randint(150, 320)
                self.direction = random.choice([1, -1])
                if self.state == PetState.IDLE_BEN:
                    self.state = PetState.WALK_BEN
                else:
                    self.state = PetState.WALK_HEATBLAST

        # State Machine Rendering
        if self.state in (PetState.IDLE_BEN, PetState.WALK_BEN, PetState.PAUSED):
            photo = self.get_current_image(self.ben_img_right, self.ben_img_left)
            self.draw_character(photo, self.draw_vector_ben)
            if photo is None:
                self.draw_omnitrix_wrist(WINDOW_W // 2 - 58, 182)

        elif self.state == PetState.ACTIVATE_OMNITRIX:
            self.state_frame += 1
            cx, cy = WINDOW_W // 2, 170
            photo = self.get_current_image(self.ben_img_right, self.ben_img_left)
            self.draw_character(photo, self.draw_vector_ben)
            self.draw_energy_ring_overlay(cx, cy)
            if photo is None:
                self.draw_omnitrix_wrist(cx - 58, 182, glow=True)

            if self.state_frame % 4 == 0:
                self.spawn_transformation_ring(radius_start=15.0 + self.state_frame * 3)

            if self.state_frame >= 18:
                self.state = PetState.TRANSFORMING_TO_HEATBLAST
                self.state_frame = 0

        elif self.state == PetState.TRANSFORMING_TO_HEATBLAST:
            self.state_frame += 1
            cx, cy = WINDOW_W // 2, 170

            # Draw rotating green energy ring portal
            self.draw_energy_ring_overlay(cx, cy)

            # Radial light beams
            for i in range(8):
                angle = math.radians(i * 45 + self.state_frame * 12)
                x2 = cx + math.cos(angle) * (60 + self.state_frame * 4)
                y2 = cy + math.sin(angle) * (60 + self.state_frame * 4)
                self.canvas.create_line(cx, cy, x2, y2, fill=OMNITRIX_GREEN, width=3)

            # Draw flashing energy orb
            orb_r = min(120, 20 + self.state_frame * 6)
            self.canvas.create_oval(cx - orb_r, cy - orb_r, cx + orb_r, cy + orb_r, fill="", outline=WHITE_HIGHLIGHT, width=4)

            if self.state_frame >= 14:
                # Reveal Heatblast mid-way through transformation
                photo = self.get_current_image(self.heat_img_right, self.heat_img_left)
                self.draw_character(photo, self.draw_vector_heatblast)
                self.spawn_heatblast_embers()
            else:
                photo = self.get_current_image(self.ben_img_right, self.ben_img_left)
                self.draw_character(photo, self.draw_vector_ben)

            if self.state_frame >= 28:
                self.state = PetState.IDLE_HEATBLAST
                self.state_frame = 0
                self.state_timer = 200

        elif self.state in (PetState.IDLE_HEATBLAST, PetState.WALK_HEATBLAST):
            photo = self.get_current_image(self.heat_img_right, self.heat_img_left)
            self.draw_character(photo, self.draw_vector_heatblast)

            # Continuous rising embers for Heatblast
            if self.frame % 2 == 0:
                self.spawn_heatblast_embers()

        elif self.state == PetState.TRANSFORMING_TO_BEN:
            self.state_frame += 1
            cx, cy = WINDOW_W // 2, 170

            self.draw_energy_ring_overlay(cx, cy)

            # Contracting fire ring
            r_contract = max(10, 120 - self.state_frame * 5)
            self.canvas.create_oval(cx - r_contract, cy - r_contract, cx + r_contract, cy + r_contract, outline=HEATBLAST_ORANGE, width=4)

            if self.state_frame >= 12:
                photo = self.get_current_image(self.ben_img_right, self.ben_img_left)
                self.draw_character(photo, self.draw_vector_ben)
            else:
                photo = self.get_current_image(self.heat_img_right, self.heat_img_left)
                self.draw_character(photo, self.draw_vector_heatblast)

            if self.state_frame >= 24:
                self.state = PetState.IDLE_BEN
                self.state_frame = 0
                self.state_timer = 200

        # Render active particle system
        self.update_particles()

        # HUD Hint banner
        self.canvas.create_text(
            10, 10,
            anchor="nw",
            text="Space / Double-Click: Transform  |  Right-Click: Menu",
            fill=OMNITRIX_GREEN,
            font=("Segoe UI", 8, "bold"),
        )

        # Schedule next tick (~33ms = ~30 FPS)
        self.root.after(33, self.tick)


def main():
    root = tk.Tk()
    Ben10PetEngine(root)
    root.mainloop()


if __name__ == "__main__":
    main()
