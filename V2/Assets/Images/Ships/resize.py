from PIL import Image
import os

_, _, filenames = next(os.walk("./"))
for file in filenames:
    if file.startswith("Starship4"):
        image = Image.open(file)
        image = image.resize((550, 200))
        image.save(file)
