import time
s = time.time()

import civilization, webpage, utils
import world as word
import sys

height = 225
width = 225

utils.remove_dir_content("./output/civs")

def show_world():
	return word.World(width, height, civs_num=5, roughness=0.45, isolationism=1.6, coldness=0.4, dryness=0.8)

show_world()

webpage.web_wrapper()

print(time.time() -s)

