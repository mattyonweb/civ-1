import random

class CivPol():
	def __init__(self, civ):
		self.civ = civ
		self.mayor = None
		self.governo = self.find_governo()

	def find_governo(self):
		''' Elabora e ritorna la forma di governo per la civiltà. '''
		convinzione = self.civ.convinzione
		ateismo = True if len(self.civ.gods)==0 else False
		
		detentori = ["nessuno", "uno", "consilium"]
		legittimatori = ["dio", "popolo", "forza"]

		#se la religiosità di un popolo è alta, allora è più probabile
		#che ottenga una teocrazia
		if convinzione > 90 and not ateismo:
			teo_bias = convinzione/5 - 17 #dà per scontato che ci siano tre scelte tra i legittimatori
		#se invece sono atei (anche poco) convinti, non saranno mai teocrazia
		elif convinzione > 60 and ateismo:
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
		["teocrazia assolutistica", "autoritarianismo", "tirannide"],
		["teocrazia oligarchica", "democrazia", "oligarchia"]]

		#per gli indici fai riferimento alla tabella qui sopra
		governo = corrispondences[detentori.index(det)][legittimatori.index(leg)]

		
		if detentori.index(det) == 0: #se nessuno è detentore del potere (ancap)
			self.mayor = "-"
			
		elif detentori.index(det) == 1: #se è uno solo
			self.mayor = self.accettable_citizen(age=18)
			self.mayor.roles.append("presidente")
			
		else: #se è un consilium
			parlamentari = list()
			while len(parlamentari) < random.randint(4,10):
				c = self.accettable_citizen()
				if c not in parlamentari:
					c.roles.append("parlamentare")
					parlamentari.append(c)
			#genera (nome_del_consiglio, lista parlamentari)s
			self.mayor = (self.civ.lang.generate_text(3).title(), parlamentari)

		return governo

	def accettable_citizen(self, num=1, age=18):
		''' Ritorna un cittadino con delle certe caratteristiche '''
		while True:
			c = random.choice(self.civ.citizens)
			if c.age >= age:
				return c
			
	def return_organi_costituzionali(self):
		return self.mayor, self.governo

	def return_informations(self):
		s = "Forma di governo: " + self.governo + "\n"
		s += self.beautify_governo()
		return s

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
			return ""
