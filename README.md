# 🟢 Ben 10 Desktop Pet

An interactive, animated desktop companion app featuring **Ben 10** and **Heatblast** built with Python, Tkinter, and Pillow for Windows 10/11.

![Ben 10 Desktop Pet Demo](assets/ben10.png)

---

## ✨ Features

- **Borderless & Transparent Window**: Floating desktop pet on top of ordinary windows.
- **Dual Character Forms**:
  - 👦 **Ben Tennyson**: Classic Ben 10 character with glowing Omnitrix on wrist.
  - 💥 **Heatblast**: Fire alien form with rising flame embers and thermal body glow aura.
- **Interactive Omnitrix Activation**:
  - Multistage energy ring expansion, neon green radial light beams, and particle bursts.
  - Smooth 6-phase transformation pipeline between Ben and Heatblast.
- **Natural Desktop Companion Behavior**:
  - Horizontal movement, boundary rebound, facing direction flips (`FLIP_LEFT_RIGHT`).
  - Idle bobbing, breathing motion, randomized pauses, and hopping animation.
  - Drag-and-drop window positioning across desktop monitors.
- **Rich User Controls**:
  - Keyboard shortcuts, double-click gestures, and custom Right-Click Context Menu.
- **Automatic Asset Preprocessing**:
  - Automatic white background removal and alpha channel transparency extraction.
  - High-resolution procedural vector artwork fallbacks if image files are missing.

---

## 🛠️ Technology Stack

- **Python 3.10+**
- **Tkinter**: Window management, borderless transparency, event handling, vector canvas.
- **Pillow (PIL)**: High-quality image loading, background removal, aspect scaling, directional flipping.

---

## 🚀 Installation & Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/ranjiths112007/Desktop-pets.git
   cd Desktop-pets
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Character Assets**:
   Place your transparent PNG character art in the `assets/` folder:
   - `assets/ben10.png` — Ben Tennyson character image
   - `assets/heatblast.png` — Heatblast character image

   *Note: If JPGs or raw screenshots are provided, the built-in loader automatically extracts transparent PNGs.*

4. **Run the Application**:
   ```bash
   python main.py
   ```
   *or:*
   ```bash
   python ben10_pet.py
   ```

---

## 🎮 Controls & Shortcuts

| Action | Control | Description |
| :--- | :--- | :--- |
| **Transform Form** | `Space` / `Double-Click` | Activates Omnitrix energy sequence and transforms pet |
| **Move Pet** | `Left-Click Drag` | Drag pet window anywhere on your screen |
| **Context Menu** | `Right-Click` | Opens pop-up menu with form toggle, hop, pause, and settings |
| **Hop / Jump** | Menu -> `Hop` | Triggers a cute parabolic jump animation |
| **Pause / Resume** | Menu -> `Pause` | Toggles walking movement on or off |
| **Close Pet** | `Escape` / Menu -> `Exit` | Closes the desktop pet application |

---

## 🧪 Testing

Run the automated test suite:
```bash
python tests/test_assets.py
```

---

## ⚠️ Disclaimer

This is a non-commercial, fan-made open-source desktop pet project. **Ben 10**, the **Omnitrix**, **Heatblast**, and related characters, names, and indicia are trademarks of and copyright Cartoon Network / Warner Bros. Discovery. This project is for personal learning and educational demonstration purposes only.
