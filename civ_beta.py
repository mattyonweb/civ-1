import civilization as cv
import cmd, random, engine

class DebugCivilta(cv.Civilta):
	def __init__(self):
		cv.Civilta.__init__(self, "", True)
		self.mayor = None
		self.governo = self.find_governo()

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
			self.mayor = random.choice(self.citizens)
			self.mayor.roles.append("presidente")
			
		else: #se è un consilium
			parlamentari = random.sample(self.citizens, random.randint(2,10))
			for p in parlamentari:
				p.roles.append("parlamentare")
			#genera (nome_del_consiglio, lista parlamentari)s
			self.mayor = (self.lang.generate_text(3).title(), parlamentari)

		return governo
			

	def print_informations(self):
		cv.Civilta.print_informations(self)
		print("Forma di governo:", self.governo)
		print(self.beautify_governo())

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

		
civ = DebugCivilta()
civ.print_informations()

class Lolicon(cmd.Cmd):
	def emptyline(self):
		civ = DebugCivilta()
		civ.print_informations()

interpreter = Lolicon()
interpreter.cmdloop()
