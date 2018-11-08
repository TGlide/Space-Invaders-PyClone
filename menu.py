import time

from helpers import *

# PPlay dependencies
from PPlay.font import *
from PPlay.window import *

def menu(wn):
	title = Font("Space Invaders", font_family=font_path("arcadeclassic"),
              size=100, color=(255, 255, 255), local_font=True)
	title.set_position(wn.width/2 - title.width/2, 50)

	play = Font("Play", font_family=font_path("arcadeclassic"),
              size=75, color=(255, 255, 255), local_font=True)
	play.set_position(wn.width/2 - play.width/2, title.y + title.height + 150)

	dificuldade = Font("Dificuldade", font_family=font_path("arcadeclassic"),
              size=75, color=(255, 255, 255), local_font=True)
	dificuldade.set_position(wn.width/2 - dificuldade.width/2, play.y + play.height + 50)

	placar = Font("Placar", font_family=font_path("arcadeclassic"),
              size=75, color=(255, 255, 255), local_font=True)
	placar.set_position(wn.width/2 - placar.width/2, dificuldade.y + dificuldade.height + 50)

	sair = Font("Sair", font_family=font_path("arcadeclassic"),
              size=75, color=(255, 255, 255), local_font=True)
	sair.set_position(wn.width/2 - sair.width/2, dificuldade.y + dificuldade.height + 50)



	options = [play, dificuldade, placar]

	selection_arrow = Font("!", font_family=font_path("arcadeclassic"),
              size=100, color=(255, 255, 255), local_font=True)
	selection_idx = 0
	selection_time_counter = time.time()

	mouse = wn.get_mouse()
	mouse_timer = time.time()

	while True:
		wn.set_background_color((0,0,0))
		
		title.draw()
		for option in options:
			option.draw()

		selection_idx = -1
		for option in options:
			if mouse.is_over_object(option):
				selection_idx = options.index(option)
				if mouse.is_button_pressed(1) and time.time() - mouse_timer > 0.1:
					return selection_idx

		if selection_idx != -1:
			selection = options[selection_idx]
			selection_arrow.set_position(selection.x - selection_arrow.width, selection.y)
			selection_arrow.draw()


		wn.update()