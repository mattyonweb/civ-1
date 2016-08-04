import world as word
import civilization, cmd

height = 400
width = 400

def show_world():
	world = word.World(width, height)
	for _ in range(5):
		civ = civilization.Civilta(world)

	world.nearest_civ_distance()
	civilization.Civilta.print_all_informations()
	world.show_image()

		
show_world()
