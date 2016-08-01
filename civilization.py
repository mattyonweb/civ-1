import engine, random

''' TODO: Ognuno deve avere la sua lingua! '''
lang = engine.Language()

class Civilta():
	civs = list()
	
	def __init__(self, world):
		self.x = 0
		self.y = 0
		self.lang = engine.Language()
		self.nome = self.lang.generate_word()
		self.population = random.randint(40, 60)

		self.religion, self.gods, self.religion_resume = self.create_religion()
		
		world.add_new_civ(self)
		Civilta.civs.append(self)

	def print_informations(self):
		print("Nome:", self.nome)
		print("Coordinate:", (self.x, self.y))
		print("Popolazione:", self.population)
		#print("Religione:", self.religion)
		#print("Dei:", ",".join(self.gods))
		self.print_resume()
		
	def print_resume(self):
		print(self.religion_resume)

	@staticmethod
	def print_all_informations():
		for civ in Civilta.civs:
			civ.print_informations()
			print("------------")

	def create_religion(self):
		god_exist = True if random.random() < 0.7 else False

		if god_exist:
			#int. 1: solo 1 dio; 2: solo più dei; 3: o 1 o 2
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

		resume = self.religion_resume(religion, gods_list)
		return (religion, gods_list, resume)

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
				
