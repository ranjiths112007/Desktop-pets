"""Launcher for Ben 10 Desktop Pet."""

import sys
import tkinter as tk
from pathlib import Path

# Ensure local directory is in PYTHONPATH
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from ben10_pet import Ben10PetEngine


def main():
    root = tk.Tk()
    app = Ben10PetEngine(root)
    root.mainloop()


if __name__ == "__main__":
    main()
