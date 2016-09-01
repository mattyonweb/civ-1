import random

class CivEco():
	def __init__(self, civ):
		self.civ = civ
		self.distanza_acqua = self.civ.sea_distance

		self.sostentamento, self.cibo, self.prod_k = self.economia_di_base()

	def economia_di_base(self):
		bio = self.civ.biome
		
		sostentamento = ["pesca", "allevamento", "agricoltura"]
		if self.civ.sea_distance > 25:
			sostentamento.remove("pesca")
		for critical_biome in ("montagna", "deserto", "congelata", "bollente"):
			if critical_biome in bio:
				sostentamento.remove("agricoltura")
				break

		stock_iniziale = self.civ.population

		produzione = 2
		if "temperata" in bio:
			produzione *= 1.5
		elif "calda" in bio or "fredda" in bio:
			produzione *= 1.05
		else:
			produzione *= 0.8

		if "deserto" in bio or "montagna" in bio:
			produzione *= 0.8
		elif "prateria" in bio:
			produzione *= 1.05
		elif "foresta" in bio or "bosco" in bio:
			produzione *= 1.5

		return sostentamento, stock_iniziale, produzione

	def return_informations(self):
		s = "Modi di sostentamento: " + ", ".join(self.sostentamento)
		s += "\nCibo ora presente: " + str(self.cibo)
		s += "\nProduttività cibo: " + str(self.prod_k)
		return s

	def grow(self):
		pass
	
			
