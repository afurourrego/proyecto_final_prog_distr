

#import random,os,sys,math #socket
#import pygame as pg
from script import *

from script.tiled_lvl import Tiled,SPACEMAP,lvl_map
from script.mission import Mission
from script.interface import Interface

class Game:

	def __init__(self,SURFACE,lvl_map):

		self.player = None
		self.load()


		#Map
		self.lvl_map = lvl_map
		SPACEMAP = 42

		#Temp
		self.lvl = "lvl_0"
		self.tile = Tiled(self.lvl_map[self.lvl],self)
		self.mission = Mission(self)

		#Surface
		self.surface = SURFACE
		self.WIDTH = self.surface.get_width()
		self.HEIGHT =  self.surface.get_height()

		self.tile_image = self.tile.make_map(SPACEMAP)



	def load(self):
		#__GROUP__#

		self.bullets = pg.sprite.Group()
		self.enemies = pg.sprite.Group()
		self.sprites = pg.sprite.Group()
		self.obs = pg.sprite.Group()
		self.objs = pg.sprite.Group()
		self.effect = pg.sprite.Group()

	def update(self):

		self.enemies.update()
		self.sprites.update()
		self.objs.update()
		self.bullets.update()
		self.mission.update()
		self.effect.update()

		self.draw()

	def draw(self):

		self.surface.blit(self.tile_image,(0,0))
		self.bullets.draw(self.surface)
		self.objs.draw(self.surface)
		self.enemies.draw(self.surface)
		self.effect.draw(self.surface)
		self.sprites.draw(self.surface)

def loop():

	map_tmp = lvl_map['lvl_0']

	WIDTH = len(map_tmp[0])*SPACEMAP
	HEIGHT = len(map_tmp)*SPACEMAP

	SCREEN = pg.display.set_mode((WIDTH,HEIGHT + 42))
	SURFACE = pg.Surface((WIDTH,HEIGHT))

	pg.display.set_caption(" Lemon Tank ")

	exit = False
	clock = pg.time.Clock()
	game = Game(SURFACE,lvl_map)
	interface = Interface(game)

	while exit != True:

		clock.tick(60)
		for event in pg.event.get():
			if event.type == pg.QUIT:
				exit = True

			if event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					exit = True
				if event.key == pg.K_SPACE:
					if game.player.cannon.load == True:
						game.player.cannon.fire = True
				elif event.key == pg.K_LEFT:
					game.player.rotate(1)
				elif event.key == pg.K_RIGHT:
					game.player.rotate(-1)
				elif event.key == pg.K_UP:
					game.player.move_bool = 1

			elif event.type == pg.JOYBUTTONUP:
				if event.button == 3: game.player.cannon.fire = True

			if event.type == pg.JOYHATMOTION:
				game.player.rotate(event.value[0] * -1) if event.value[0] != 0 else 0
				game.player.move_bool = 1 if event.value[1] == 1 else 0
			if event.type == pg.KEYUP:
				if event.key == pg.K_UP:
					game.player.move_bool = 0


		game.update()
		SCREEN.blit(SURFACE,(0,0))
		interface.update()
		interface.draw(SCREEN)

		pg.display.flip()

if __name__ == "__main__":

	loop()
	pg.quit()
