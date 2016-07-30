from PIL import Image, ImageDraw, ImageFont
import noise, random, engine
height = 600
width = 300

class World():

	def __init__(self, x, y):
		self.width = x
		self.height = y
		#attenzione: alla heightmap bisogna accedere così:
		#self.heightmap[y][x] e non il contrario!!!
		self.heightmap = self.create_bit_list(8, 0.8, 2.6)
		self.civs = {}
		self.img = self.create_image()

	def create_bit_list(self, octave=2, persistence=0.5, lacunarity=2.0):
		random_start = random.random()*1134.72864
		l = []
		for y in range(height):
			l1 = []
			for x in range(width):
				value = abs(int(noise.snoise2(random_start + x/1751, random_start + y/1571,
											octave, persistence, lacunarity)*255))
				l1.append(value)
			l.append(l1)
		return l

	def create_image(self):
		img = Image.new( 'RGB', (self.width, self.height), "black") # create a new black image
		pixels = img.load()

		#0-60: blu mare
		#60-85 giallo spiagge
		#86-150 verde foresta
		#151-200 grigio montagna
		#200-255 bianco neve
		for y in range(img.size[1]):
			for x in range(img.size[0]):
				val = self.heightmap[y][x]
				if val < 55:
					c = (45+2*val,45+2*val,255)
				elif val >= 55 and val < 60:
					c = (255,255,50)
				elif val >=60 and val <90:
					c = (0,300-val,0)
				elif val >= 90 and val <130:
					c = (128,128,128)
				else:
					c = (255,255,255)
				pixels[x,y] = c #le coordinate boh
		return img
		
	def show_image(self):
		#self.create_image().show()
		self.img.show()
		for civ in self.civs:
			print(civ.nome, self.civs[civ])
		
	def add_new_civ(self, civ_obj):
		self.civs[civ_obj] = civ_obj.x0, civ_obj.y0
		self.mark_civ_on_map(civ_obj)
		
	def mark_civ_on_map(self, civ_obj, r=10):
		x = civ_obj.x0
		y = civ_obj.y0
		name = civ_obj.nome
		draw = ImageDraw.Draw(self.img)
		draw.ellipse((x-r, y-r, x+r, y+r), fill = 'red', outline ='white')
		draw.ellipse((x-r/5, y-r/5, x+r/5, y+r/5), fill = 'white', outline ='white')

		font = ImageFont.truetype("Ticketing.ttf",15)
		draw.text((x+r,y+r),name + " " + str(x) + "," + str(y),(0,0,0), font=font)
#------------------------------

class Civilta():
	def __init__(self, world, nome):
		self.nome = nome
		self.x0, self.y0 = self.place_civilta(world)
		world.add_new_civ(self)

	def place_civilta(self, world):
		while True:
			x, y = random.randint(0, width-1), random.randint(0,height-1)
			if world.heightmap[y][x] >=55: #forse è il contrario
				return x, y

#----------------------------------

world = World(width, height)
lang = engine.Language()
for _ in range(15):
	civ = Civilta(world, lang.generate_word())

world.show_image()
