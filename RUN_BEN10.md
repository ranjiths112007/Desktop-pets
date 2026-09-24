# Run the Ben 10 pet

## 1. Clone the repository

```bash
git clone https://github.com/ranjiths112007/Desktop-pets.git
cd Desktop-pets
```

## 2. Install the dependency

```bash
python -m pip install -r requirements.txt
```

## 3. Add your images

Create an `assets` folder and copy your files into it:

- `assets/ben10.jpg` — the Ben Tennyson image you supplied
- `assets/heatblast.png` — the Heatblast image you supplied

The Ben image is cropped to its right side automatically to remove the logo area. Near-white pixels are made transparent.

## 4. Start

```bash
python ben10_pet.py
```

## Controls

- **Double-click** or **Space**: activate the Omnitrix and transform
- **Left-click + drag**: move the pet
- **Right-click** or **Escape**: close the pet

If the images are missing, the app uses a simple vector fallback so the program still launches.
