import civilization
import world as word

height = 512
width = 512

def show_world():
	world = word.World(width, height, 6, 0.45)
		
	world.nearest_civ_distance()
	world.distances_water()
	civilization.Civilta.print_all_informations()
	world.show_image()
	world.save_images()

for _ in range(1):
	show_world()
