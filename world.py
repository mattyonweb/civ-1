from PIL import Image, ImageDraw, ImageFont
import noise, random, math, civilization

class World():

	def __init__(self, x, y):
		self.width = x
		self.height = y

		self.sea_level = 45
		self.mount_level = 90
		#attenzione: alla heightmap bisogna accedere così:
		#self.heightmap[y][x] e non il contrario!!!
		self.heightmap = self.create_matrix("height", 8, 0.8, 2.6) #matrix altezze
		self.tempmap = self.create_matrix("temp", 7, 0.9, 2.1) #la matrix delle temperature
		self.rainmap = self.create_matrix("rain", 8, 0.9, 2.1)
		self.civs = {} #dizionario civ_obj:(x,y)
		self.img = self.create_heightmap_image() #immagine del mondo
		
	# --- GENERATION ---
	def create_matrix(self, layer="height", octave=2, persistence=0.5, lacunarity=2.0):
		random_start = random.random()*1134.72864
		
		l = []
		for y in range(self.height):
			l1 = []
			for x in range(self.width):
				base_val = noise.snoise2(random_start + x/1751, random_start + y/1571,
											octave, persistence, lacunarity)
				if layer == "height":
					val = abs(int(base_val*255))
					
				elif layer == "temp":					
					h = self.heightmap[y][x]
					if h > self.mount_level:
						delta = h * 4/165 + 1
					else:
						delta = 1
					val = abs(int(base_val*350/delta))
					
				elif layer == "rain":
					val = self.maprange(base_val, -1, 1, 0, 255)

				l1.append(val)
			l.append(l1)
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
					c = (45+2*val,45+2*val,255)
				elif val >= self.sea_level and val < 60:
					c = (255,255,50)
				elif val >=60 and val <self.mount_level:
					c = (0,300-val,0)
				elif val >= self.mount_level and val <130:
					c = (128,128,128)
				else:
					c = (255,255,255)
				pixels[x,y] = c #le coordinate boh
		return img

	def create_tempmap_image(self):
		''' Ritorna l'immagine delle temperature; bianco è più caldo, e vic. '''
		img = Image.new( 'RGB', (self.width, self.height), "black")
		pixels = img.load()

		for y in range(img.size[1]):
			for x in range(img.size[0]):
				val = self.tempmap[y][x]
				pixels[x,y] = (int(val*350/255), int(val*350/255), int(val*350/255))
		return img

	def create_rainmap_image(self):
		img = Image.new( 'RGB', (self.width, self.height), "black")
		pixels = img.load()

		for y in range(img.size[1]):
			for x in range(img.size[0]):
				val = self.rainmap[y][x]
				pixels[x,y] = (int(val/2), int(val/2), int(val/2))
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
		self.img.show()

	# --- CIV INTERFACES ---
		
	def add_new_civ(self, civ):
		''' Procedura per aggiungere civiltà al mondo.
		Prima le si aggiunge al dizionario delle civiltà;
		poi le si marca sulla cartina del territorio '''
		civ.x, civ.y = self.place_civ()
		self.civs[civ] = civ.x, civ.y
		self.mark_civ_on_map(civ)

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

	# --- UTILS ---
	def bell_curve(self, x, a, b, c):
		return a*math.e**((-(x-b)**2)/2*c**2)

	def maprange(self, s,a1,a2,b1,b2):
		return b1+(((s-a1)*(b2-b1))/(a2-a1))
		

#----------------------------------
