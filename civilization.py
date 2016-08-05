import engine, random

class Civilta():
	civs = list()
	
	def __init__(self, world, debug=False):
		self.debug = debug
		
		self.x = 0
		self.y = 0

		self.lang = engine.Language()
		self.nome = self.lang.generate_word()
		
		self.population = random.randint(40, 60)
		self.citizens = self.create_citizens()

		self.religion, self.gods, self.religion_resume, self.convinzione = self.create_religion()

		self.mayor = None
		self.governo = self.find_governo()

		self.biome = ""
		self.nearest = ()
		if not self.debug:
			world.add_new_civ(self)
		
		Civilta.civs.append(self)

	def __str__(self):
		return self.nome

	def print_informations(self):
		print("Nome:", self.nome)
		print("Coordinate:", (self.x, self.y))
		if not self.debug:
			print("Civiltà più vicina:", str(self.nearest[1]), self.nearest[0])
		print("Popolazione:", self.population)
		print("Bioma:", self.resume_biome())
		print("Religione:", self.religion_resume)
		print("Convinzione nella metafisica:", self.convinzione)
		print("Forma di governo:", self.governo)
		print(self.beautify_governo())

		
	@staticmethod
	def print_all_informations():
		''' Stampa le informazioni di TUTTE le civ, con un separatore '''
		for civ in Civilta.civs:
			civ.print_informations()
			print("------------")

	def create_citizens(self):
		''' Crea e salva tutti i cittadini. '''
		return [Citizen(self) for _ in range(self.population)]

	def find_governo(self):
		''' Elabora e ritorna la forma di governo per la civiltà. '''
		
		detentori = ["nessuno", "uno", "consilium"]
		legittimatori = ["dio", "popolo", "forza"]

		#se la religiosità di un popolo è alta, allora è più probabile
		#che ottenga una teocrazia
		if self.convinzione > 90 and len(self.gods) != 0:
			teo_bias = self.convinzione/5 - 17 #dà per scontato che ci siano tre scelte tra i legittimatori

		#se invece sono atei (anche poco) convinti, non saranno mai teocrazia
		elif self.convinzione > 65 and len(self.gods) == 0:
			teo_bias = 0
		else:
			teo_bias = 1

		#montecarlo per decidere i detentori del potere
		while True:
			det = random.choice(detentori)
			if random.random() < 1/(2*len(detentori)):
				break

		#montecarlo pesato per decidere l'origine del potere
		while True:
			leg = random.choice(legittimatori)

			if leg == "dio":
				if random.random() < teo_bias/len(legittimatori):
					break
			else:
				if random.random() < 1/(2*len(legittimatori)):
					break

		#tabella che funziona così:
		#sulle y (dall'alto), detentori: nessuno, uno, consilium
		#sulle x, legittimatori: dio, popolo, forza
		corrispondences = [
		["anarchia utopica", "anarchia libertaria", "anarchia militare"],
		["teocrazia assolutistica", "autoritarianismo", "oligarchia"],
		["teocrazia oligarchica", "democrazia", "tirannide"]]

		#per gli indici fai riferimento alla tabella qui sopra
		governo = corrispondences[detentori.index(det)][legittimatori.index(leg)]

		
		if detentori.index(det) == 0: #se nessuno è detentore del potere (ancap)
			self.mayor = "-"
			
		elif detentori.index(det) == 1: #se è uno solo
			while True:
				c = random.choice(self.citizens)
				if random.randint(10, 100) < c.age:
					break
			self.mayor = c
			self.mayor.roles.append("presidente")
			
		else: #se è un consilium
			parlamentari = random.sample(self.citizens, random.randint(2,10))
			for p in parlamentari:
				p.roles.append("parlamentare")
			#genera (nome_del_consiglio, lista parlamentari)s
			self.mayor = (self.lang.generate_text(3).title(), parlamentari)

		return governo

	def beautify_governo(self):
		if isinstance(self.mayor, Citizen):
			return "Presidente: " + str(self.mayor)
		elif isinstance(self.mayor, tuple):
			s = "Nome del consilium: " + str(self.mayor[0]) + "\nAppartenenti:\n\t"
			for c in self.mayor[1]:
				s += str(c) + "\n\t "
			return s
		else:
			return "-"

	def create_religion(self):
		''' Crea una religione.
		Ritorna (Tipo religione, lista_degli_Dei, riassunto) '''
		god_exist = True if random.random() < 0.7 else False

		if god_exist:
			#1: solo 1 dio; 2: solo più dei; 3: o 1 o 2
			religions = { 
				"Deismo" : 3,
				"Monoteismo" : 1, 
				"Enoteismo" : 2,
				"Politeismo" : 2 }

			religion = random.choice(list(religions.keys()))

			if religions[religion] == 1:
				gods_num = 1
			elif religions[religion] == 2:
				gods_num = random.randint(2, 10)
			else:
				if random.random() < 0.4:
					gods_num = 1
				else:
					gods_num = random.randint(2, 10)

			gods_list = [self.lang.generate_word().capitalize() for _ in range(gods_num)]

		else:
			religion = random.choice(["Animismo", "Agnosticismo", "Ateismo"])
			gods_list = []

		convinzione = random.randint(50,100)

		resume = self.religion_resume(religion, gods_list)
		return (religion, gods_list, resume, convinzione)


	def religion_resume(self, religion, gods):
		if religion == "Ateismo":
			s = random.choice([
			"Non vi è una religione diffusa, in generale vi è disinteresse nei confronti dell'ultraterreno.",
			"La popolazione è prevalentemente atea, priva di interesse nei confronti dell'aldilà."
			"Dio, o gli dei, non ricadono negli interessi della popolazione." ])

		elif religion == "Agnosticismo":
			s = random.choice([
			"La popolazione non sa se credere o no in qualche Dio, rifugiandosi nell'esercizio del dubbio."])

		elif religion == "Animismo":
			s = random.choice([
			"Sebbene non esista un Dio di riferimento, la maggior parte delle persone crede nell'esistenza di una forza vitale all'interno di tutte le cose.",
			"Un pneuma, secondo i locali, esiste in tutti gli oggetti, gli animali e le persone, anche se la natura di questo soffio non trascende la natura stessa."])

		elif religion == "Deismo":
			if len(gods) > 1:
				s = random.choice([
				"Secondo la popolazione, esistono divinità creatrici di tutte le cose, che però non toccano gli uomini e non li influenzano.",
				"La gente generalmente riconosce l'esistenza di Dei, ma senza lasciarsi influenzare troppo dalla loro presenza.",
				"La loro religione stabilisce l'esistenza di alcuni principii primi, che tuttavia non modificano il corso della storia umana."])
				s += "Gli dei in questione sono: " + ",".join(gods)
			else:
				s = random.choice([
				"Secondo la popolazione, esiste una divinità creatrice di tutte le cose, che però non tocca gli uomini e non li influenza.",
				"La gente generalmente riconosce l'esistenza di Dio, ma senza lasciarsi influenzare troppo dalla sua presenza.",
				"La loro religione stabilisce l'esistenza di un principio primo, che tuttavia non modifica il corso della storia umana."])
				s += "Il dio in questione è " + gods[0]

		elif religion == "Monoteismo":
			s = random.choice([
				"La gente adora e venera un solo dio: ",
				"La religione è pratica diffusa presso questa civiltà, in particolare per quanto riguarda il Dio ",
				])
			s += gods[0]

		elif religion == "Enoteismo":
			s = random.choice([
			"Sebbene il Pantheon indichi la presenza di diverse divinità, una in particolare viene lodata e adorata:",
			"Ufficialmente di religione politeista, questo popolo concentra le proprie preghiere soprattutto su "])
			s += gods[0]
			s += ". Gli altri dei sono: " + ",".join(gods[1:])

		elif religion == "Politeismo":
			s = random.choice([
			"La religione è tipicamente politeista. Gli dei sono: ",
			"La gente del posto adora più di un dio: "])
			s += ",".join(gods)

		return s

	def resume_biome(self):
		return self.biome

class Citizen:
	def __init__(self, civ):
		self.civ = civ
		self.nome = " ".join( (civ.lang.generate_word().capitalize() for _ in range(2)))
		self.age = random.randint(0, 99)
		self.sex = random.choice(["m","f"])
		self.roles = []

	def __str__(self):
		s = ", ".join((self.nome, self.sex, str(self.age)))
		if len(self.roles) > 0:
			s += " (" + ", ".join(self.roles) + ")"
		return s
