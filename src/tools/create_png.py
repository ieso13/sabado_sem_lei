from PIL import Image, ImageDraw
from dfs.lista_jogos import lista_jogos_df
import numpy as np

jogadores = lista_jogos_df["Jogador"].unique()

print(jogadores)

for i in jogadores:
    jogador = i.replace(" ", "-")
    img = Image.new("RGB", (255, 255), "rgb(0,0,0)")
    # img.save(f"C:/Code/sabado_sem_lei/src/assets/fotos_func/{jogador}.png", "PNG")
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
        f"C:/Code/sabado_sem_lei/src/assets/fotos_func/{jogador}.png"
    )
