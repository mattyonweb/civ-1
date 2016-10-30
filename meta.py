import time
s = time.time()

import civilization
import world as word
import sys
#sys.stdout = open('file', 'w')

height = 350
width = 600

def show_world():
	world = word.World(width, height, civs_num=11, roughness=0.45, isolationism=1.6, coldness=0.4, dryness=0.8)
	civilization.Civilta.print_all_informations()
	return world

show_world()
print(time.time() -s)

