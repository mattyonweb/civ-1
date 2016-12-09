import time
s = time.time()

import civilization, webpage, utils
import world as word
import sys
#sys.stdout = open('file', 'w')

height = 475
width = 650

utils.remove_dir_content("./output/civs")

def show_world():
	world = word.World(width, height, civs_num=15, roughness=0.45, 
isolationism=1.6, coldness=0.4, dryness=0.8)
	#civilization.Civilta.print_all_informations()
	return world

show_world()

webpage.web_wrapper()

print(time.time() -s)

