import world, civilization

height = 400
width = 750

world = world.World(width, height)
for _ in range(15):
	civ = civilization.Civilta(world)

world.save_images()
civilization.Civilta.print_all_informations()
world.show_image()
