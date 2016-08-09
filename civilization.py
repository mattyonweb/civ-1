import engine, random, utils
import civpol, civrel

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

		self.religione = civrel.CivRel(self)
		self.religion, self.gods, self.role, self.reward, self.adoration = self.religione.return_teogonia(resume=False)
		self.convinzione = int( sum(c.convinzione for c in self.citizens) / len(self.citizens))
		
		self.politics = civpol.CivPol(self)
		self.mayor, self.governo = self.politics.return_organi_costituzionali()

		self.biome = ""
		self.nearest = ()
		if not self.debug:
			world.add_new_civ(self)
		
		Civilta.civs.append(self)

	def __str__(self):
		return self.nome

	def print_informations(self):
		print(self.return_base_informations())
		print(self.religione.return_informations())
		print(self.politics.return_informations())

	def return_base_informations(self):
		s = "Nome: " + self.nome
		s += "\nCoordinate: " + str((self.x, self.y))
		if not self.debug:
			s += "\nCiviltà più vicina: " + str(self.nearest) 
		s += "\nPopolazione: " + str(self.population)
		s += "\nBioma: " + self.resume_biome()
		s += "\nConvinzione: " + str(self.convinzione)
		return s
		
	@staticmethod
	def print_all_informations():
		''' Stampa le informazioni di TUTTE le civ, con un separatore '''
		for civ in Civilta.civs:
			civ.print_informations()
			print("------------")

	def create_citizens(self):
		''' Crea e salva tutti i cittadini. '''
		return [Citizen(self) for _ in range(self.population)]

	def resume_biome(self):
		return self.biome         


class Citizen:
	def __init__(self, civ):
		self.civ = civ
		self.nome = " ".join( (civ.lang.generate_word().capitalize() for _ in range(2)))
		self.age = random.randint(0, 99)
		self.sex = random.choice(["m","f"])
		self.roles = []
		self.convinzione = utils.random_montecarlo_bell(0.9, 0.5, 4.5) * 100

	def __str__(self):
		s = ", ".join((self.nome, self.sex, str(self.age)))
		if len(self.roles) > 0:
			s += " (" + ", ".join(self.roles) + ")"
		return s
