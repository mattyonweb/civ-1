import random

class CivPol():
	detentori = ["nessuno", "uno", "consilium"]
	legittimatori = ["dio", "popolo", "forza"]
	
	#tabella che funziona così:
	#sulle y (dall'alto), CivPol.detentori: nessuno, uno, consilium
	#sulle x, CivPol.legittimatori: dio, popolo, forza
	corrispondences = [
	["anarchia utopica", "anarchia libertaria", "anarchia militare"],
	["teocrazia assolutistica", "autoritarianismo", "tirannide"],
	["teocrazia oligarchica", "democrazia", "oligarchia"]]

	def __init__(self, civ):
		self.civ = civ

		religious_bias = self.return_religious_bias()
		detentore = self.return_montecarlo_choice_from(CivPol.detentori)
		legittimatore = self.return_montecarlo_choice_from(CivPol.legittimatori, religious_bias, "dio")
		
		self.governo = self.return_politics_definition(detentore, legittimatore)
		self.mayor = self.return_mayor(detentore, legittimatore)
	

	def return_politics_definition(self, det, leg):
		''' Ritorna il nome-definizione esatto per la propria
		forma politica in base ai detentori e legittimatori del potere. '''
		return CivPol.corrispondences[CivPol.detentori.index(det)][CivPol.legittimatori.index(leg)]
		
	def return_mayor(self, det, leg):
		''' Ritorna un numero consono di cittadini_obj
		che ricoprano la carica di sindaco. '''
		if CivPol.detentori.index(det) == 0: #se nessuno è detentore del potere (ancap)
			return "-"
			
		elif CivPol.detentori.index(det) == 1: #se è uno solo
			citizen = self.return_accettable_citizen(age=18)
			citizen.roles.append("presidente")
			if leg == "dio":
				citizen.roles.append("autorità spirituale")
			return citizen
			
		else: #se è un consilium
			parlamentari = list()
			while len(parlamentari) < random.randint(4,10):
				c = self.return_accettable_citizen()
				if c not in parlamentari:
					c.roles.append("parlamentare")
					if leg == "dio":
						c.roles.append("porporato")
					parlamentari.append(c)
			#genera (nome_del_consiglio, lista parlamentari)s
			return (self.civ.lang.generate_text(3).title(), parlamentari)

	def return_religious_bias(self):
		''' Ritorna il bias riguardante la religione '''
		ateismo = True if len(self.civ.religione.gods_list)==0 else False
		convinzione = self.civ.convinzione
		
		if not ateismo and convinzione > 90:
			return convinzione/5 - 17
		elif ateismo:
			return 0
		else:
			return 1

	def return_montecarlo_choice_from(self, pool, bias=1, bias_condition=None):
		while True:
			choice = random.choice(pool)

			if choice == bias_condition:
				if random.random() < bias/len(pool):
					return choice
			else:
				if random.random() < 1/len(pool):
					return choice
					
	def return_accettable_citizen(self, age=18):
		''' Ritorna un cittadino con delle certe caratteristiche '''
		while True:
			c = random.choice(self.civ.citizens)
			if c.age >= age:
				return c
			
	def return_organi_costituzionali(self):
		return self.mayor, self.governo

	def return_informations(self):
		s = "----- POLITICA -----\n"
		s += "Forma di governo: " + self.governo + "\n"
		s += self.beautify_governo()
		return s + "\n\n"

	def beautify_governo(self):
		''' Abbellire il resume per quanto riguarda la politica '''
		import civilization
		
		if isinstance(self.mayor, civilization.Citizen):
			return "Presidente: " + str(self.mayor)
		elif isinstance(self.mayor, tuple):
			s = "Nome del consilium: " + str(self.mayor[0]) + "\nAppartenenti:\n\t"
			for c in self.mayor[1]:
				s += str(c) + "\n\t"
			return s
		else:
			return "Presidente: nessuno."
