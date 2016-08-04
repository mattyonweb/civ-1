from PIL import Image, ImageDraw, ImageFont
import noise, random, math, civilization, collections

class World():

	def __init__(self, x, y):
		self.width = x
		self.height = y

		self.sea_level = 45
		self.mount_level = 90
		
		#attenzione: alla heightmap bisogna accedere così:
		#self.heightmap[y][x] e non il contrario!!!
		self.heightmap = self.create_matrix("height", 8, 0.8, 2.28)
		self.tempmap = self.create_matrix("temp", 8, 0.89, 2.4, 300,400)
		self.rainmap = self.create_matrix("rain", 8, 0.89, 2.5, 400,300)
		self.biomemap = self.create_biomes_matrix()
		self.borders = self.borders()
		
		self.civs = {} #dizionario civ_obj:(x,y)
		
		self.img = self.create_heightmap_image() #immagine del mondo

	# --- GENERATION ---
	def create_matrix(self, layer="height", octave=2, persistence=0.5, lacunarity=2.0, x_diff=1751, y_diff=1571):
		random_start = random.random()*1134.72864
		cunt = []
		l = []
		for y in range(self.height):
			l1 = []
			for x in range(self.width):
				base_val = noise.snoise2(random_start + x/x_diff, random_start + y/y_diff,
											octave, persistence, lacunarity)
				
				if layer == "height":
					val = abs(int(base_val*255))
					
				elif layer == "temp":
					h = self.heightmap[y][x]
					if h > self.mount_level:
						delta = self.maprange(h, self.mount_level, 255, 1, 3)
					else:
						delta = 1
					val = int((128 + self.maprange(base_val, -1, 1, -128, 128))/delta)
					#print(val)
					
				elif layer == "rain":
					val = 128 + int(self.maprange(base_val,-1, 1, -128, 128))
					

				l1.append(val)
			l.append(l1)
		return l

	def create_biomes_matrix(self):
		l = []
		cunt = []
		for y in range(self.height):
			l1 = []
			for x in range(self.width):
				val = self.return_biome(self.heightmap[y][x], self.tempmap[y][x], self.rainmap[y][x])
				l1.append(val)
				cunt.append(val)
			l.append(l1)
		print(collections.Counter(cunt))
		return l

	def return_biome(self, h, t, mm):
		hb = {
		(0, self.sea_level) : "s",
		(self.sea_level, 75) : "p" ,
		(75, self.mount_level) : "h",
		(self.mount_level, 256) :"m"}
		
		rb = {
		(0, 85) : "d",
		(85,155) : "n",
		(155,255) : "w"}
		
		tb = {
		(0, 85) : "c",
		(85,170) : "t",
		(170,255) : "h"}
		
		biome = ""

		for limits in hb:
			if h >= limits[0] and h < limits[1]:
				biome += hb[limits]
				break

		for limits in tb:
			if t >= limits[0] and t < limits[1]:
				biome += tb[limits]
				break

		for limits in rb:
			if mm >= limits[0] and mm < limits[1]:
				biome += rb[limits]
				break

		return biome

	def borders(self):
		l = [[0 for x in range(self.width)] for y in range(self.height)]
		
		for y in range(self.height):
			for x in range(self.width):

				for _x in range(-1,2):
					for _y in range(-1,2):
						if _x != 0 and _y != 0:
							try:
								if self.biomemap[y][x] != self.biomemap[y+_y][x+_x]:
									l[y+_y][x+_x] = 1
							except:
								pass
		return l
		
	# --- PAINTING ---
	def create_heightmap_image(self):
		''' Ritorna immagine del territorio (senza civiltà, quelle vanno aggiunte
		direttamente a self.img) '''
		img = Image.new( 'RGB', (self.width, self.height), "black")
		pixels = img.load()

		#0-60: blu mare
		#60-85 giallo spiagge
		#86-150 verde foresta
		#151-200 grigio montagna
		#200-255 bianco neve
		for y in range(img.size[1]):
			for x in range(img.size[0]):
				val = self.heightmap[y][x]
				if val < self.sea_level:
					c = (50+val,55+val,255)
				elif val >= self.sea_level and val < 60:
					c = (255,255,50)
				elif val >=60 and val <self.mount_level:
					c = (0,300-val,0)
				elif val >= self.mount_level and val <110:
					c = (128,128,128)
				else:
					c = (255,255,255)
				pixels[x,y] = c
		return img

	def create_tempmap_image(self):
		''' Ritorna l'immagine delle temperature; bianco è più caldo, e vic. '''
		img = Image.new( 'RGB', (self.width, self.height), "black")
		pixels = img.load()

		for y in range(img.size[1]):
			for x in range(img.size[0]):
				val = self.tempmap[y][x]
				pixels[x,y] = (val, 0, 0)
		return img

	def create_rainmap_image(self):
		img = Image.new( 'RGB', (self.width, self.height), "black")
		pixels = img.load()

		for y in range(img.size[1]):
			for x in range(img.size[0]):
				val = self.rainmap[y][x]
				pixels[x,y] = (int(val/2), int(val/2), int(val/2))
		return img

	def create_biomes_image(self):
		hb = "sphm"; mm = "dnw"; t = "cth";
		img = Image.new( 'RGB', (self.width, self.height), (255,255,255,0))
		pixels = img.load()
		
		for y in range(img.size[1]):
			for x in range(img.size[0]):
				biome_code = self.biomemap[y][x]
				#print(biome_code)
				if biome_code[0] == "s":
					pixels[x,y] = (0,0,55)
				else:
					pixels[x,y] = (int(255*hb.index(biome_code[0])/len(hb)), int(255*t.index(biome_code[1])/len(t)), int(255*mm.index(biome_code[2])/len(mm)))
		return img

	def create_borders_image(self):
		img = Image.new( 'RGB', (self.width, self.height), (255,255,255,0))
		pixels = img.load()

		for y in range(img.size[1]):
			for x in range(img.size[0]):
				pixels[x,y] = (0,0,0) if self.borders[y][x]==1 else (255,255,255,0)
		return img

	def blend_height_temp(self, img1, img2):
		''' Ritorna l'immagine miscuglio tra temperatura e territorio '''
		return Image.blend(img1, img2, 0.55)

	def save_images(self):
		''' Salva tutte le immagini del mondo '''
		self.img.save("./output/terrain.jpg")
		self.create_tempmap_image().save("./output/temperature.jpg")
		self.create_rainmap_image().save("./output/rainfall.jpg")
		self.blend_height_temp(self.img, self.create_rainmap_image()).save("./output/blend.jpg")
		
	def show_image(self):
		''' Mostra l'immagine del territorio salvata '''
		self.create_tempmap_image().show()
		self.create_rainmap_image().show()
		self.img.show()
		self.create_biomes_image().show()
		#self.create_borders_image().show()

	# --- CIV INTERFACES ---
		
	def add_new_civ(self, civ):
		''' Procedura per aggiungere civiltà al mondo.
		Prima le si aggiunge al dizionario delle civiltà;
		poi le si marca sulla cartina del territorio '''
		civ.x, civ.y = self.place_civ()
		self.civs[civ] = civ.x, civ.y
		self.mark_civ_on_map(civ)
		civ.biome = self.biomemap[civ.y][civ.x]

	def place_civ(self):
		''' Ritorna una locazione non marina per l'insediamento della civ. '''
		while True:
			x, y = random.randint(0, self.width-1), random.randint(0, self.height-1)
			if self.heightmap[y][x] >=55:
				return x, y
				
	def mark_civ_on_map(self, civ_obj, r=10):
		''' Segnala su self.img la posizione delle cività. Da invocare ogni volta
		che self.img viene per qualche motivo ricreata! '''
		x = civ_obj.x
		y = civ_obj.y
		name = civ_obj.nome
		draw = ImageDraw.Draw(self.img)
		draw.ellipse((x-r, y-r, x+r, y+r), fill = 'red', outline ='white')
		draw.ellipse((x-r/5, y-r/5, x+r/5, y+r/5), fill = 'white', outline ='white')

		font = ImageFont.truetype("Ticketing.ttf",15)
		draw.text((x,y+r), name + " " + str(x) + "," + str(y), (0,0,0), font=font)

	def nearest_civ_distance(self):
		for civ1 in self.civs:
			min, civ = 1000, None
			for civ2 in self.civs:
				if civ1 != civ2:
					d = self.distance(civ1.x, civ2.x, civ1.y, civ2.y)
					if d < min:
						min, civ = d, civ2
			civ1.nearest = (min, civ)
					

	# --- UTILS ---
	def bell_curve(self, x, a, b, c):
		return a*math.e**((-(x-b)**2)/2*c**2)

	def maprange(self, s,a1,a2,b1,b2):
		return b1+(((s-a1)*(b2-b1))/(a2-a1))

	def distance(self, x1, x2, y1, y2):
		return math.sqrt( (x2-x1)**2 + (y2-y1)**2)
		

#----------------------------------
