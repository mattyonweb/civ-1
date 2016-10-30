from PIL import Image, ImageDraw, ImageFont
import noise, random, math, civilization, collections, time
from utils import *

class World():
	#2, 0.45, 0.4, 0.2
	def __init__(self, x, y, civs_num=2, roughness=0.45, isolationism=1.45, coldness=0.4, dryness=0.2, show_images=True, save_images=True):
		self.width = x
		self.height = y

		#i livelli delle varie altezze
		self.sea_lvl = 0.4
		self.beach_lvl = 0.42
		self.plains_lvl = 0.6
		self.hills_lvl = 0.7
		self.mountain_lvl = 0.9

		#i livelli delle varie temperature
		self.freezing_lvl = 0.1
		self.cold_lvl = 0.35
		self.temperate_lvl = 0.5
		self.warm_lvl = 0.75
		self.boiling_lvl = 1
		
		#attenzione: alla heightmap bisogna accedere così:
		#self.heightmap[y][x] e non il contrario!!!
		print("Generazione matrix")
		self.heightmap = self.create_matrix(6, 0.75, 2, exp=roughness, isolationism=isolationism)
		
		#moisture: un grande exp significa più secchezza
		self.moisturemap = self.create_matrix(6, 0.8, 2.2, 300, 300, exp=dryness)
		
		#temp: maggiore exp significa più freddezza
		self.tempmap = self.create_matrix(6, 0.8, 2.2, exp=coldness)
		
		self.biomemap = self.create_biome_matrix()

		self.islandsmap = [[0 for x in range(self.width)] for y in range(self.height)]
		self.generate_islandsmap()
		print("Fine generazione matrix")

		print("Inizio generazione vita")
		self.civs = {} #dizionario civ_obj:(x,y)
		for _ in range(civs_num):
			self.add_new_civ(civilization.Civilta(self))
		print("Fine generazione vita")
		
		self.height_img = self.return_complete_world_image()
		self.temp_img = self.create_moisturemap_image()
		self.biome_img = self.create_biomemap_image()

		#salva in ogni civiltà la rispettiva civiltà più vicina
		self.find_every_civs_nearest()
		self.find_collisions()

		if show_images:
			self.show_images()
		if save_images:
			self.save_images()

	# --- GENERATION ---
	def create_matrix(self, octave=2, persistence=0.5, lacunarity=2.0,
							x_diff=311, y_diff=311, exp=0.5, isolationism=1,
							mode="standard", rad=200, debug=False):
		''' Genera una matrice con il perlin noise.
		exp è la pendenza della funzione sigmoide, ie maggiore è exp più
		uniforme saranno i valori ritornati, minore è exp maggiori sono gli
		estremi.
		isolationism lo uso per le heightmap. un valore alto genera isole sempre
		più piccole e solitarie, un valore piccolo genera grosse masse di terra.
		'''
		
		random_start = random.random()*random.uniform(1,100)
		smooth_func = self.return_smoothing_function(mode, exp, isolationism)
		matrix = []

		for y in range(self.height):
			row = []
			for x in range(self.width):
				base_val = noise_rescale(noise.snoise2(random_start + x/x_diff,
															random_start + y/y_diff,
															octave, persistence, lacunarity))
				val = smooth_func(base_val, x, y, rad)
				row.append(val)
			matrix.append(row)

		print(avg_map(matrix)) #stampa la media di tutti questi valori
		return matrix

	def return_smoothing_function(self, mode, exp, isolationism):
		''' Ritorna una funzione che modifica un valore '''
		if mode == "standard":
			def standard_mode(x, *args):
				return (sigmoid_func(x, exp) * x) ** isolationism
			return standard_mode
			
		elif mode == "radial":	
			def radial_mode(val, x, y, rad):
				distance = (x - self.width/2)**2 + (y - self.height/2)**2
				if distance < rad**2:
					m = -distance*(1/(rad*2)) + 1.5
				else:
					m = -distance/rad + 1
				return val * m
			return radial_mode	

	def create_biome_matrix(self):
		''' Lunga e dolorsa trafila per creare una matrix di biomi. '''
		biomemap = [["" for x in range(self.width)] for y in range(self.height)]
		
		for y in range(self.height):
			for x in range(self.width):
				h = self.heightmap[y][x]
				m = self.moisturemap[y][x]
				t = self.tempmap[y][x]

				if h < self.sea_lvl:
					biomemap[y][x] = "mare"

				elif h > self.hills_lvl:
					if m < 0.1:
						biomemap[y][x] = "montagna asciutta"
					elif m < 0.4:
						biomemap[y][x] = "montagna tundrosa"
					else:
						biomemap[y][x] = "montagna nevosa"

				elif h > self.plains_lvl:
					if m < 0.2:
						biomemap[y][x] = "deserto"
					elif m <0.6:
						biomemap[y][x] = "bosco"
					else:
						biomemap[y][x] = "taiga"

				elif h > self.beach_lvl:
					if m < 0.45:
						biomemap[y][x] = "steppa"
					elif m < 0.5:
						biomemap[y][x] = "prateria"
					elif m < 0.65:
						biomemap[y][x] = "palude"
					else:
						biomemap[y][x] = "foresta pluviale"
						
				else:
					if m<0.15:
						biomemap[y][x] = "deserto"
					elif m<0.5:
						biomemap[y][x] = "spiaggia"
					else:
						biomemap[y][x] = "foresta pluviale"

				biomemap[y][x] += " " + self.return_temp_adj(t)

		return biomemap

	def find_connected_regions_first_step(self):
		''' Individua zone di terra connesse tra loro (continenti, isole, isolette
		ecc...) e le identifica con un numero.
		Questo è il primo passo per l'identificazione completa e pulita delle
		terre. '''
		seen = set() #le celle già viste. si può velocizzare togliendo quelle che non serviranno più!
		counter = 0 #per gli ID

		#vedi dopo
		equivalences = {} 
		
		for x in range(self.width):
			for y in range(self.height):
				#crea una lista neigh che contiene le celle vicine a quella in questione
				#che sono già state visitate
				neigh = list()
				for x_ in range(-1,2):
					for y_ in range(-1,2):
						if not (y_==0 and x_==0):
							if (x+x_, y+y_) in seen:
								neigh.append(self.islandsmap[y+y_][x+x_])

				#print(neigh, self.heightmap[y][x], end=", ")
				#se la cella selezionata è circondata da caselle vuote e ad essa
				#corrisponde, in heightmap, un punto di terra emersa, dichiara una
				#nuova isola
				if neigh.count(0) == len(neigh) and self.heightmap[y][x] > self.sea_lvl:
					counter += 1
					self.islandsmap[y][x] = counter
					
				elif self.heightmap[y][x] <= self.sea_lvl:
					self.islandsmap[y][x] = 0

				#altrimenti, si assegna alla cella in questione l'id più piccolo tra
				#quelli nel neigh. in caso di conflitti (ie quando ci sono più id isola
				#nello stesso neigh) si assegna al dizionario equivalences un record:
				#equivalences[id_grande] = id_minore
				#per poter, in seguito, riunire tutto in un unica isola
				else:
					unique_values_neigh = set(neigh) #gli id presenti nel neigh
					try:
						unique_values_neigh.remove(0)
					except:
						pass
						
					if len(unique_values_neigh) > 1:
						for _ in range(len(unique_values_neigh)-1):
							equivalences[max(unique_values_neigh)] = min(unique_values_neigh)
							unique_values_neigh.remove(max(unique_values_neigh))

					self.islandsmap[y][x] = min(unique_values_neigh)
				
				seen.add((x,y))
		return equivalences

	def generate_islandsmap(self):
		''' Rimuove le impurità lasciate dal primo step e completa il lavoro
		unificando le isole che in realtà sono un'unica terra. '''
		print("Identificazione isole - inizio")
		start_time = time.time()
		equivalences = self.find_connected_regions_first_step()
		for x in range(self.width):
			for y in range(self.height):
				self.islandsmap[y][x] = self.find_root(equivalences, self.islandsmap[y][x])
		print("Fine identificazione isole - tempo:", time.time() - start_time)

	def find_root(self, d, value):
		''' Risale alla radice delle references presenti in equivalences.
		siccome eq. è della forma: {60:45, 45:32:, 32:4}, di fatto l'isola con
		ID=60 è equivalente all'isola con ID=4. Questa funzione partendo dal
		value 60 ritorna 4. '''
		if value not in d.keys():
			return value
		else:
			return self.find_root(d, d[value])

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
	''' FONDAMENTALE PER LA TRASPARENZA:
	l'immagine di base (img) deve essere in formato "RBG", e la maschera che ci
	andrà sopra (draw) in "RGBA", sennò non funziona!!!!! '''
	
	def create_heightmap_image(self):
		''' Ritorna immagine del territorio (senza civiltà, quelle vanno aggiunte
		direttamente a self.height_img) '''
		img = Image.new('RGB', (self.width, self.height), (255,255,255,0))
		pixels = img.load()

		for y in range(img.size[1]):
			for x in range(img.size[0]):
				height = self.heightmap[y][x]
				pixels[x,y] = self.height_color_old_effect(height)			
		return img

	def create_biomemap_image(self, temp_on=False):
		''' Idem per biomi '''
		img = Image.new('RGB', (self.width, self.height), (255,255,255,0))
		pixels = img.load()

		for y in range(img.size[1]):
			for x in range(img.size[0]):
				b = self.biomemap[y][x]
				pixels[x,y] = self.biome_color(b, temp_on)			
		return img

	def create_moisturemap_image(self):
		''' Idem per umidità '''
		img = Image.new( 'RGB', (self.width, self.height), (255,255,255,0))
		pixels = img.load()

		for y in range(img.size[1]):
			for x in range(img.size[0]):
				val = self.moisturemap[y][x]
				pixels[x,y] = (int(val*255), int(val*255), int(val*255))
		return img

	def draw_borders_on(self, background_image):
		''' Disegna i confini terra-mare sopra un'altraimmagine '''
		img = background_image
		pixels = img.load()

		for y in range(img.size[1]):
			for x in range(img.size[0]):
				try:
					#n sono i vicini, n0 la posizione attuale da analizzare
					n = set(self.biomemap[y+y_][x+x_] for y_ in range(-1, 2) for x_ in range(-1, 2) if x_!=y_)
					n0 = self.biomemap[y][x]
					for cell in n:
						if ("mare" in cell and not "mare" in n0) or (not "mare" in cell and "mare" in n0):
							pixels[x,y] = (112,110,89)
							break
				except: 
					continue

		return img
		
	def island_img(self):
		img = Image.new( 'RGB', (self.width, self.height), (255,255,255,0))
		pixels = img.load()
		colors = self.islands_colors()
		
		for y in range(img.size[1]):
			for x in range(img.size[0]):
				pixels[x,y] = colors[self.islandsmap[y][x]]
		return img
				
	def return_complete_world_image(self, old_effect=True):
		return self.mark_civs_on_map(self.draw_borders_on(self.create_heightmap_image()))

	# --- COLORAZIONI ---

	def height_color(self, height):
		''' Colorazioni per le diverse altitudini '''
		if height < self.sea_lvl:
			c = (int(height*200),int(height*200),255)					
		elif height < self.beach_lvl:
			c = (255,255,0)					
		elif height < self.plains_lvl:
			c = (int(maprange(height,0.4,0.6,255,0)),255,0)					
		elif height < self.hills_lvl:
			c = (128,128,128)					
		else:
			c = (int(height*300),int(height*300),int(height*300))
		return c

	def height_color_old_effect(self, height):
		''' Colorazioni per le diverse altitudini - effetto antico '''
		if height < self.sea_lvl:
			c = (211-int(height*100),194-int(height*100),170-int(height*100))
					
		else:
			c = (int(maprange(height,0.4,1,191,255)),
				int(maprange(height,0.4,1,174,255)),
				int(maprange(height,0.4,1,150,255)))
		return c

	def islands_colors(self):
		''' Un colore per ogni isola '''
		colors = {}
		# set() elimina tutte le occorrenze multiple all'interno di una lista
		for ids in set((self.islandsmap[y][x] for y in range(self.height) for x in range(self.width))):
			colors[ids] = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
		return colors
		
	def biome_color(self, biome, temperature=True):
		b = biome
		if "mare" in b:
			col = (64,64,255)
		elif "spiaggia" in b:
			col = (255,255,0)
		elif "montagna" in b:
			col = (255,255,255)
		elif "deserto" in b or "steppa" in b:
			col = (200,200,64)
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
		if temperature:
			if "congelata" in b:
				c = blend_colors(col, (32,32,200))
			elif "fredda" in b:
				c = blend_colors(col, (128,128,255))
			if "temperata" in b:
				c = col
			elif "calda" in b:
				c = blend_colors(col, (255,128,129))
			elif "bollente" in b:
				c = blend_colors(col, (200,32,32))
			return c
		else:
			return col

	def save_images(self):
		''' Salva tutte le immagini del mondo '''
		self.height_img.save("./output/terrain.jpg")
		
	def show_images(self):
		''' Mostra l'immagine del territorio salvata '''
		self.mark_civs_on_map(self.draw_borders_on(self.draw_roads_on(self.height_img))).show()
		self.island_img().show()



	# --------------------- CIV INTERFACES ---------------------
		
	def add_new_civ(self, civ):
		''' Procedura per aggiungere civiltà al mondo.
		Prima le si aggiunge al dizionario delle civiltà;
		poi le si marca sulla cartina del territorio '''
		#non toccare le seguenti due righe, vanno bene così fidati
		civ.x, civ.y = self.place_civ()
		self.civs[civ] = civ.x, civ.y
		civ.biome = self.biomemap[civ.y][civ.x]
		civ.territori = self.return_civ_territories(civ)
		

	def place_civ(self):
		''' Ritorna una locazione non marina per l'insediamento della civ. '''
		while True:
			x, y = random.randint(0, self.width-1), random.randint(0, self.height-1)
			
			# fa in modo di non mettere civilta troppo vicine tra loro
			for civ in self.civs:
				if distance(civ.x, civ.y, x, y) > 40:
					continue
					
			# non permette civiltà nel mare
			if self.heightmap[y][x] >= self.sea_lvl:
				return x, y
				
	def mark_civs_on_map(self, img, r=5):
		''' Segnala su self.height_img la posizione delle cività. Da invocare ogni volta
		che self.height_img viene per qualche motivo ricreata! '''
		draw = ImageDraw.ImageDraw(img, 'RGBA')
		
		for civ in self.civs:
			x = civ.x
			y = civ.y
			name = civ.nome
			p = civ.population
			
			draw.ellipse((x-r, y-r, x+r, y+r), fill = 'red', outline ='white')
			draw.ellipse((x-r/5, y-r/5, x+r/5, y+r/5), fill = 'white', outline ='white')
			draw.ellipse((x-p/2, y-p/2, x+p/2, y+p/2), fill = (random.randint(0,255),random.randint(0,255),random.randint(0,255),64))
			font = ImageFont.truetype("arial.ttf",15)
			draw.text((x,y+r), name, (0,0,0), font=font)

		return img

	def draw_roads_on(self, img, connectness = 0.85):
		''' Calcola e disegna le strade. '''
		draw = ImageDraw.ImageDraw(img, 'RGBA')

		#insieme delle civiltà già collegate (per evitare di fare strade da A a
		#B e da B ad A, raddoppiando il tempo di esecuzione dello script
		permutations = set()
		#i = 0

		print("Avvio calcolo e disegno delle strade")
		for civ1 in self.civs:
			for civ2 in self.civs:
				if civ1 != civ2:
					if self.islandsmap[civ1.y][civ1.x] != self.islandsmap[civ2.y][civ2.x]:
						continue
					elif (civ1,civ2) in permutations or (civ2,civ1) in permutations:
						continue
					else:
						if random.random() < 1-connectness:
							print("Non-collegamento casuale tra", civ1.nome, civ2.nome)
							permutations.add((civ1,civ2))
							permutations.add((civ2,civ1))
							continue
						print("Inizio collegamento", civ1.nome, civ2.nome)
						start_time = time.time()
						permutations.add((civ1,civ2))
						path_coord = find_path(self.heightmap, civ1.x,civ1.y,civ2.x,civ2.y, self.sea_lvl, self.mountain_lvl)
						if path_coord is None:
							print(civ1.nome, civ2.nome, "Le due civ sono sulla stessa isola ma utils/find_path non trova una strada fra le due. BUG")
							continue
						for coord in path_coord:
							x = coord[0]
							y = coord[1]
							draw.point((x, y), fill = (112,110,89))
						print("Collegate civiltà:", civ1.nome, civ2.nome, "--- tempo:", start_time-time.time())
		print("Fine calcolo e disegno delle strade")
		return img

	def find_every_civs_nearest(self):
		''' Per ogni civiltà civ1, trova la civiltà civ2 più vicina e la salva
		in civ1.nearest '''
		print("Calcolo delle città più vicine")
		start = time.time()
		
		for civ1 in self.civs:
			min, civ = math.inf, None
			for civ2 in self.civs:
				if civ1 != civ2:
					d = distance(civ1.x, civ2.x, civ1.y, civ2.y)
					if d < min:
						min, civ = d, civ2
			civ1.nearest = (min, str(civ))
		print("Fine calcolo città vicine", time.time()-start)

	def return_civ_territories(self, civ):
		''' Ritorna un insieme di tutte le coordinate (x,y) sotto il controllo
		di una cività civ. '''
		coordinates_set = set()
		for x in range(civ.x-int(civ.population/2),civ.x+int(civ.population/2)):
			for y in range(civ.y-int(civ.population/2),civ.y+int(civ.population/2)):
				if (x-civ.x)**2+(y-civ.y)**2 < (civ.population**2)/4:
					coordinates_set.add((x,y))
		return coordinates_set

	def find_collisions(self):
		''' STAMPA (per ora) i territori di due civiltà che si sovrappongono '''
		for civ1 in self.civs:
			for civ2 in self.civs:
				if civ1!=civ2 and not civ1.territori.isdisjoint(civ2.territori):
					if civ1 not in civ2.territori_contesi.keys():
						print("Territori contesi", civ1.nome, civ2.nome)
						civ1.territori_contesi[civ2] = civ1.territori.intersection(civ2.territori)
						civ1.relazioni[civ2] = "g"
						civ2.territori_contesi[civ1] = civ1.territori.intersection(civ2.territori)
						civ2.relazioni[civ1] = "g"

