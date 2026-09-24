# 🚀 Ben 10 Desktop Pet Quickstart Guide

Follow these simple steps to run your Ben 10 Desktop Pet on Windows 10/11.

## 1. Setup Environment

Open your terminal or Command Prompt in the project folder:

```bash
pip install -r requirements.txt
```

## 2. Run the Pet Engine

You can start the pet using either launcher command:

```bash
python main.py
```

or:

```bash
python ben10_pet.py
```

## 3. Controls Quick Reference

- **Space Bar** or **Double-Click**: Activate Omnitrix & Transform into Heatblast (or return to Ben).
- **Left Mouse Click + Drag**: Drag Ben or Heatblast anywhere on your desktop screen.
- **Right Mouse Click**: Open the Context Menu (Transform, Hop, Pause/Resume, Exit).
- **Escape Key**: Instantly close the application.

## 4. Run Automated Tests

To verify asset loading and state machine logic:

```bash
python tests/test_assets.py
```
