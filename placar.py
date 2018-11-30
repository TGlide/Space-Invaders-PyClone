from helpers import *

# PPlay dependencies
from PPlay.font import *
from PPlay.window import *

def placar(wn):
    with open("placar.txt", "r") as f:
        scores = [Font(line.replace("\n", ""), font_family=font_path("arcadeclassic"), size=75, 
        color=(255,255,255), local_font=True) for line in f.readlines()]
    for score in range(len(scores)):
        scores[score].set_position(0, score*(scores[0].height + 10))

    while True:
        wn.set_background_color((0,0,0))

        for score in scores:
            score.draw()

        wn.update()

if __name__ == "__main__":
    placar(Window(1200, 900))