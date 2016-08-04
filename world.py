from PIL import Image, ImageDraw, ImageFont
import noise, random, math, civilization, collections

class World():

	def __init__(self, x, y):
		self.width = x
		self.height = y

		#i livelli delle varie altezze
		self.sea_lvl = 0.2
		self.beach_lvl = 0.22
		self.plains_lvl = 0.4
		self.hills_lvl = 0.5
		self.mountain_lvl = 0.7

		#i livelli delle varie temperature
		self.freezing_lvl = 0.1
		self.cold_lvl = 0.35
		self.temperate_lvl = 0.5
		self.warm_lvl = 0.75
		self.boiling_lvl = 1
		
		#attenzione: alla heightmap bisogna accedere così:
		#self.heightmap[y][x] e non il contrario!!!
		self.heightmap = self.create_matrix(6, 0.75, 2.31, exp=2.6)
		self.moisturemap = self.create_matrix(6, 0.8, 2.2, 300,300, exp=1)
		self.tempmap = self.create_matrix(6, 0.8, 2.2, exp=2.1)
		self.biomemap = self.create_biome_matrix()
		
		self.civs = {} #dizionario civ_obj:(x,y)
		
		self.img = self.create_heightmap_image() #immagine del mondo

	# --- GENERATION ---
	def create_matrix(self, octave=2, persistence=0.5, lacunarity=2.0, x_diff=311, y_diff=311, exp=3):
		''' Genera una matrice con il perlin noise.
		exp è il rapporto tra gli estremi: ad es, un valore alto di exp per le
		altezze porterà ad una altezza media più bassa (quindi più mare), e
		viceversa. '''
		random_start = random.random()*random.uniform(1,100)
		
		l = []
		for y in range(self.height):
			l1 = []
			for x in range(self.width):
				base_val = self.noise_rescale(noise.snoise2(random_start + x/x_diff,
															random_start + y/y_diff,
															octave, persistence, lacunarity))
				val = base_val ** exp					
				l1.append(val)
			l.append(l1)
		print(self.avg_map(l)) #stampa la media di tutti questi valori
		return l

	def create_biome_matrix(self):
		''' Lunga e dolorsa trafila per creare una matrix di biomi. '''
		biome_matrix = [["" for x in range(self.width)] for y in range(self.height)]
		
		for y in range(self.height):
			for x in range(self.width):
				h = self.heightmap[y][x]
				m = self.moisturemap[y][x]
				t = self.tempmap[y][x]

				if h < self.sea_lvl:
					biome_matrix[y][x] = "mare"

				elif h > self.hills_lvl:
					if m < 0.1:
						biome_matrix[y][x] = "montagna asciutta"
					elif m < 0.4:
						biome_matrix[y][x] = "montagna tundrosa"
					else:
						biome_matrix[y][x] = "montagna nevosa"

				elif h > self.plains_lvl:
					if m < 0.2:
						biome_matrix[y][x] = "deserto"
					elif m <0.6:
						biome_matrix[y][x] = "bosco"
					else:
						biome_matrix[y][x] = "taiga"

				elif h > self.beach_lvl:
					if m < 0.1:
						biome_matrix[y][x] = "deserto"
					elif m < 0.5:
						biome_matrix[y][x] = "prateria"
					elif m < 0.7:
						biome_matrix[y][x] = "palude"
					else:
						biome_matrix[y][x] = "foresta pluviale"
						
				else:
					if m<0.15:
						biome_matrix[y][x] = "deserto"
					elif m<0.5:
						biome_matrix[y][x] = "spiaggia"
					else:
						biome_matrix[y][x] = "foresta pluviale"

				biome_matrix[y][x] += " " + self.return_temp_adj(t)

		return biome_matrix

	def return_temp_adj(self, value):
		''' Ritorna l'aggettivo corrispondente alla temperatura value.
		Da aggiustare perché non tiene conto dei maschili/femminili '''
		if value < self.freezing_lvl:
			return "congelata"
		elif value < self.cold_lvl:
			return "fredda"
		elif value < self.temperate_lvl:
			return "temperata"
		elif value < self.warm_lvl:
			return "calda"
		else:
			return "bollente"

						
	# --- PAINTING ---
	
	def create_heightmap_image(self):
		''' Ritorna immagine del territorio (senza civiltà, quelle vanno aggiunte
		direttamente a self.img) '''
		img = Image.new( 'RGB', (self.width, self.height), "black")
		pixels = img.load()

		for y in range(img.size[1]):
			for x in range(img.size[0]):
				val = self.heightmap[y][x]
				
				if val < self.sea_lvl:
					c = (0,0,255)
					
				elif val < self.beach_lvl:
					c = (255,255,0)
					
				elif val < self.plains_lvl:
					c = (0,255,0)
					
				elif val < self.hills_lvl:
					c = (128,128,128)
					
				else:
					c = (255,255,255)
				pixels[x,y] = c
				
		return img

	def create_biomemap_image(self, temp_on=False):
		img = Image.new( 'RGB', (self.width, self.height), "black")
		pixels = img.load()

		for y in range(img.size[1]):
			for x in range(img.size[0]):
				b = self.biomemap[y][x]
				if "mare" in b:
					col = (64,64,255)
				elif "spiaggia" in b:
					col = (255,255,0)
				elif "montagna" in b:
					col = (255,255,255)
				elif "deserto" in b:
					col = (200,200,50)
				elif "bosco" in b:
					col = (0,128,0)
				elif "prateria" in b:
					col = (0,255,0)
				elif "taiga" in b:
					col = (40,150,200)
				elif "foresta" in b:
					col = (30,80,30)
				elif "palude" in b:
					col = (70,60,60)
				else:
					col = (0,0,0)

				if temp_on:
					if "congelata" in b:
						c = self.blend_colors(col, (32,32,200))
					elif "fredda" in b:
						c = self.blend_colors(col, (128,128,255))
					if "temperata" in b:
						c = col
					elif "calda" in b:
						c = self.blend_colors(col, (255,128,129))
					elif "bollente" in b:
						c = self.blend_colors(col, (200,32,32))

					pixels[x,y]=c
				else:
					pixels[x,y]=col
					
		return img
					
					
	def create_moisturemap_image(self):
		img = Image.new( 'RGB', (self.width, self.height), "black")
		pixels = img.load()

		for y in range(img.size[1]):
			for x in range(img.size[0]):
				val = self.moisturemap[y][x]
				pixels[x,y] = (int(val*255), int(val*255), int(val*255))
		return img

	def blend_height_temp(self, img1, img2):
		''' Ritorna l'immagine miscuglio tra temperatura e territorio '''
		return Image.blend(img1, img2, 0.75)

	def save_images(self):
		''' Salva tutte le immagini del mondo '''
		self.img.save("./output/terrain.jpg")
		#self.create_tempmap_image().save("./output/temperature.jpg")
		#self.create_rainmap_image().save("./output/rainfall.jpg")
		#self.blend_height_temp(self.img, self.create_rainmap_image()).save("./output/blend.jpg")
		
	def show_image(self):
		''' Mostra l'immagine del territorio salvata '''
		#self.create_tempmap_image().show()
		self.img.show()
		#self.create_moisturemap_image().show()

		all_biomes = (self.biomemap[y][x] for y in range(self.height) for x in range(self.width))
		print(collections.Counter(all_biomes))

		self.create_biomemap_image().show()
		self.blend_height_temp(self.create_biomemap_image(), self.create_biomemap_image(True)).show()
		#self.create_biomes_image().show()
		#self.create_borders_image().show()



	# --------------------- CIV INTERFACES ---------------------
		
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
			if self.heightmap[y][x] >=self.sea_lvl:
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
		''' Per ogni civiltà civ1, trova la civiltà civ2 più vicina e la salva
		in civ1.nearest ''' 
		for civ1 in self.civs:
			min, civ = 1000, None
			for civ2 in self.civs:
				if civ1 != civ2:
					d = self.distance(civ1.x, civ2.x, civ1.y, civ2.y)
					if d < min:
						min, civ = d, civ2
			civ1.nearest = (min, str(civ))
					

	# --- UTILS ---
	def bell_curve(self, x, a, b, c):
		return a*math.e**((-(x-b)**2)/2*c**2)

	def maprange(self, s,a1,a2,b1,b2):
		return b1+(((s-a1)*(b2-b1))/(a2-a1))

	def noise_rescale(self, val):
		''' Porta il noise da [-1,1] a [0,1]'''
		return 0.5 + val/2

	def distance(self, x1, x2, y1, y2):
		return math.sqrt( (x2-x1)**2 + (y2-y1)**2)

	def avg_map(self, mappa):
		''' Ritorna la media dei valori di una matrix '''
		all_vals = (mappa[y][x] for y in range(len(mappa)) for x in range(len(mappa[1])))
		return sum(all_vals)/(len(mappa)*len(mappa[1]))

	def blend_colors(self, c1, c2):
		''' Missa due colori. '''
		f = lambda x,y: int(255-(( (255-x)**2 + (255-y)**2)/2)**0.5)
		#f = lambda x,y: min(x+y,255)
		new_r = f(c1[0],c2[0])
		new_g = f(c1[1],c2[1])
		new_b = f(c1[2],c2[2])
		return (new_r, new_g, new_b)
