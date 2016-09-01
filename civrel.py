import random

class CivRel():
	gods_role = [
	"creazione",
	"provvidenza",
	"nessuno" ]
	
	rel_ricompensa = [
	"paradiso",
	"favori",
	"nessuna",
	"taumaturgia" ]
	
	adoration = ["preghiere", "sacrifici", "costruzioni", "jiad", "nessuna",
	"canti", "flagellamento", "riti sessuali", "proselitismo", "meditazione",
	"giochi"]
	
	def __init__(self, civ):
		self.civ = civ
		kind, gods, role, reward, adoration  = self.create_religion()

		self.religion = kind
		self.gods_list = gods
		self.gods_role = role
		self.reward = reward
		self.adoration = adoration
		
	def create_religion(self):
		''' Crea una religione.
		Ritorna (Tipo religione, lista_degli_Dei, riassunto) '''
		kind, num, role, reward, adoration = self.choice_religion_property()
		gods_list = [(self.civ).lang.generate_word().capitalize() for _ in range(num)]

		return kind, gods_list, role, reward, adoration

	def choice_religion_property(self):
		gods_numerology = {
		"Monotesimo" : 1,
		"Enoteismo" : random.randint(2, 8),
		"Politeismo" : random.randint(3, 10) }

		''' Se dio esiste, allora è tutto normale;
		se dio non esiste, al 36% sarà una religione ma senza un dio,
		al 64% sarà una civiltà atea. '''
		god_exist = True if random.random() < 0.7 else False #se c'è uno o più dio
		theism = True if not god_exist and random.random() < 0.26 else False #se si crede in una religione

		# ["nessuno"] è una lista perché così posso fare ", ".join(lista)
		if not god_exist and not theism:
			return ("Ateismo", 0, ["nessuno"], ["nessuna"], ["nessuna"])
			
		elif not god_exist and theism:
			return ("Outeismo", 0, ["nessuno"], ["nessuna"], ["nessuna"])
			
		else:
			rel = random.choice(list(gods_numerology.keys()))
			gods_num = gods_numerology[rel]
			gods_rol = self.exclusive_choices(CivRel.gods_role) 
			ricompensa = self.exclusive_choices(CivRel.rel_ricompensa)
			adorazione = self.exclusive_choices(CivRel.adoration)
			return (rel, gods_num, gods_rol, ricompensa, adorazione)
			

	def exclusive_choices(self, tab):
		''' Ritorna una o più scelte coerenti tra loro. Ad esempio: se in gods_role
		c'è la scelta "nessuno", si possono fare tutte le altre scelte presenti
		in gods_role ma se tra queste vi è anche "nessuno" allora vengono scartate. '''
		max_len = len(tab) - 1
		num = random.randint(1, max_len)

		while True:
			choices = random.sample(tab, num)
			if not "nessuno" in choices and not "nessuna" in choices:
				return choices
			elif len(choices) == 1 and (choices == "nessuno" or choices == "nessuna"):
				return choices
				
	def return_teogonia(self, resume=True):
		return self.religion, self.gods_list, self.gods_role, self.reward, self.adoration

	def return_informations(self):
		s = "Religione: " + self.religion
		if self.religion == "Ateismo":
			return s
			 
		s += "\nDio/Dei:"
		if self.gods_list == []:
			s += "-"
		else:
			for god in self.gods_list:
				s += "\n\t" + god
		s += "\nAzioni di Dio: " + ", ".join(self.gods_role)
		s += "\nRicompensa religione: " + ", ".join(self.reward)
		s += "\nMetodi di adorazione: " + ", ".join(self.adoration)
		return s
