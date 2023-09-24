import os
from PIL import Image, ImageDraw
import numpy as np

directory_in_str = "C:/Users/zanat/OneDrive/Área de Trabalho/fotos"

directory = os.fsencode(directory_in_str)

for file in os.listdir(directory):
    filename = os.fsdecode(file)
    img = Image.open(f"C:/Users/zanat/OneDrive/Área de Trabalho/fotos/{filename}")
    img = img.resize((255, 255))
    filename = filename.replace(" ", "-")
    img = img.convert("RGB")
    npImage = np.array(img)
    h, w = img.size
    # Create same size alpha layer with circle
    alpha = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(alpha)
    draw.pieslice([0, 0, h, w], 0, 360, fill=255)

    # Convert alpha Image to numpy array
    npAlpha = np.array(alpha)

    # Add alpha layer to RGB
    npImage = np.dstack((npImage, npAlpha))

    # Save with alpha
    Image.fromarray(npImage).save(
        f"C:/Code/sabado_sem_lei/src/assets/fotos_func/{filename}"
    )
