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

	gods_numerology = {
	0 : "Ateismo",
	1 : "Monoteismo",
	2 : "Politeismo" }
	
	def __init__(self, civ):
		self.civ = civ
		
		self.num_of_gods = self.return_number_of_gods()
		self.religion_definition = self.return_religion_definition()
		self.gods_list = self.return_gods_list()
		self.gods_role = self.coherent_choices_for(CivRel.gods_role)
		self.reward = self.coherent_choices_for(CivRel.rel_ricompensa)
		self.adoration = self.coherent_choices_for(CivRel.adoration)

		self.libro_sacro = self.civ.lang.generate_book_title()

	def return_number_of_gods(self):
		return 0 if random.random() < 0.2 else random.randint(1,8)
		
	def return_gods_list(self):
		''' Ritorna una lista di nomi di dei. '''
		return [(self.civ).lang.generate_word().capitalize() for _ in range(self.num_of_gods)]

	def return_religion_definition(self):
		''' Ritorna una stringa del tipo Monoteismo, Ateismo o Politeismo '''
		if self.num_of_gods in CivRel.gods_numerology.keys():
			return CivRel.gods_numerology[self.num_of_gods]
		else:
			return "Politeismo"			

	def coherent_choices_for(self, tab):
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
		return self.religion_definition, self.gods_list, self.gods_role, self.reward, self.adoration

	def return_informations(self):
		s = "Religione: " + self.religion_definition
		if self.religion_definition == "Ateismo":
			return s
		s += "\nLibro sacro: " + self.libro_sacro
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
