from PIL import Image, ImageDraw, ImageFont
import noise, random, engine, math
height = 400
width = 750

class World():

	def __init__(self, x, y):
		self.width = x
		self.height = y
		#attenzione: alla heightmap bisogna accedere così:
		#self.heightmap[y][x] e non il contrario!!!
		self.heightmap = self.create_heightmap(8, 0.8, 2.6) #matrix altezze
		self.tempmap = self.create_tempmap() #la matrix delle temperature
		self.civs = {} #dizionario civ_obj:(x,y)
		self.img = self.create_image() #immagine del mondo


	# --- GENERATION ---
	def create_heightmap(self, octave=2, persistence=0.5, lacunarity=2.0):
		''' Ritorna la heightmap matrix '''
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

	def create_tempmap(self, octave=7, persistence=0.9, lacunarity=2.1):
		''' Ritorna la tempmap matrix '''
		random_start = random.random()*1134.72864
		l = []
		for y in range(height):
			l1 = []
			for x in range(width):
				#val = self.bell_curve(y, 350, height/2, (50*10**-3))
				val = abs(int(noise.snoise2(random_start + x/1751, random_start + y/1571,
											octave, persistence, lacunarity)*350))
				h = self.heightmap[y][x]
				if h > 90:
					delta = h * 4/165 + 1
				else:
					delta = 0
				l1.append(val-delta)
			l.append(l1)
		return l


	# --- PAINTING ---
	def create_image(self):
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

	def tempmap_image(self):
		''' Ritorna l'immagine delle temperature; bianco è più caldo, e vic. '''
		img = Image.new( 'RGB', (self.width, self.height), "black")
		pixels = img.load()

		for y in range(img.size[1]):
			for x in range(img.size[0]):
				val = self.tempmap[y][x]
				pixels[x,y] = (int(val*350/255), int(val*350/255), int(val*350/255))
		return img

	def blend_height_temp(self):
		''' Ritorna l'immagine miscuglio tra temperatura e territorio '''
		return Image.blend(self.img, self.tempmap_image(), 0.55)

	def save_images(self):
		''' Salva tutte le immagini del mondo '''
		self.img.save("./output/terrain.jpg")
		self.tempmap_image().save("temperature.jpg")
		self.blend_height_temp().save("blend.jpg")
		
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
			x, y = random.randint(0, width-1), random.randint(0, height-1)
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
		
#------------------------------

class Civilta():
	def __init__(self, world, nome):
		self.nome = nome
		self.x, self.y = 0, 0
		world.add_new_civ(self)

#----------------------------------

world = World(width, height)
lang = engine.Language()
for _ in range(15):
	civ = Civilta(world, lang.generate_word())

world.save_images()
world.show_image()
