import engine, random, utils
import civpol, civrel, civeco

class Civilta():
	civs = list()
	
	def __init__(self, world, debug=False):
		self.debug = debug

		self.x = 0
		self.y = 0

		#lingua e nome della cività
		self.lang = engine.Language()
		self.nome = self.lang.generate_word().capitalize()

		#citizens è la lista di tutti i cittadini_obj
		self.genealogic_graph = {}
		self.citizens = self.create_citizens()
		self.population = len(self.citizens)

		self.religione = civrel.CivRel(self)
		self.convinzione = int( sum(c.convinzione for c in self.citizens) / len(self.citizens))
		
		self.politics = civpol.CivPol(self)

		self.biome = ""
		self.nearest = () #nearest_city - distance o il contrario
		self.sea_distance = 500
		self.territori = None

		Civilta.civs.append(self)
		if not self.debug:
			world.add_new_civ(self)

		self.economia = civeco.CivEco(self)
		self.territori_contesi = {} #la forma è: civiltà:lista-di-territorii
		self.relazioni = {}
		self.save_informations()

	def __str__(self):
		return self.nome

	def print_informations(self):
		print(self.return_base_informations())
		print(self.lang.return_informations())
		print(self.religione.return_informations())
		print(self.politics.return_informations())
		print(self.economia.return_informations())

	def save_informations(self):
		import os
		dire = os.path.dirname(__file__)
		filename = os.path.join(dire, './output/civs/' + self.nome)
		f = open(filename, "w")
		f.write(self.return_base_informations()+"\n")
		f.write(self.lang.return_informations()+"\n")
		f.write(self.religione.return_informations()+"\n")
		f.write(self.politics.return_informations()+"\n")
		f.write(self.economia.return_informations()+"\n")
		

	def return_base_informations(self):
		s = "Nome: " + self.nome
		s += "\nCoordinate: " + str((self.x, self.y))
		if not self.debug:
			s += "\nCiviltà più vicina: " + str(self.nearest)
		s += "\nPopolazione: " + str(self.population)
		s += "\nBioma: " + self.biome
		s += "\nDistanza dall'acqua: " + str(self.sea_distance)
		s += "\nConvinzione: " + str(self.convinzione)
		#s += str(self.territori_contesi))
		if self.relazioni:
			s += "\nRelazioni con le altre civiltà:"
			for civ in self.relazioni:
				s += "\n\tciv.nome" + ": " + self.relazioni[civ]
		s += "\nAlberi genealogici:"
		for parents, sons in self.genealogic_graph.items():
			if not sons:
				continue
			s += "\n" + " + ".join(str(parent) for parent in parents) + " = "
			s += " , ".join(str(son) for son in sons)
		return s + "\n"
		
	@staticmethod
	def print_all_informations():
		''' Stampa le informazioni di TUTTE le civ, con un separatore '''
		for civ in Civilta.civs:
			civ.print_informations()
			print("------------")

	@staticmethod
	def generate_html_links():
		s = "<html><head><meta charset='UTF-8'></head><body>"
		for civ in Civilta.civs:
			s += "<a href='./civs/" + civ.nome + "'>" + civ.nome + "</a><br>"
		return s + "</body></html>"
		
	def create_citizens(self):
		''' Crea e salva tutti i cittadini. '''
		#return [Citizen(self) for _ in range(self.population)]
		all_citizens = []
		for num_families in range(random.randint(10,30)):
			male = Citizen(self, "m", min_age=18, max_age=60)
			female = Citizen(self, "f", min_age=18, max_age=60)
			sons = [Citizen(self, random.choice(("m", "f")), min_age=0, max_age=6) for _ in range(random.randint(0,3))]
			
			self.genealogic_graph[(male, female)] = sons
			all_citizens.append(male)
			all_citizens.append(female)
			for son in sons:
				all_citizens.append(son)
		return all_citizens
			

class Citizen:
	def __init__(self, civ, sex, min_age=0, max_age=99):
		self.civ = civ
		self.nome = " ".join( (civ.lang.generate_word().capitalize() for _ in range(2)))
		self.age = random.randint(min_age, max_age)
		self.sex = sex
		self.roles = []
		self.convinzione = utils.random_montecarlo_bell(0.9, 0.5, 4.5) * 100

	def __str__(self):
		s = ", ".join((self.nome, self.sex, str(self.age)))
		if len(self.roles) > 0:
			s += " (" + ", ".join(self.roles) + ")"
		return s
