import numpy as np

def fatigueStrength(shaft):

	def Ka():
		if shaft.finish == 'ground':
			return 1.58*shaft.Sut**-0.085
		elif shaft.finish == 'machined':
			return 4.51*shaft.Sut**-0.265
		elif shaft.finish == 'cold-drawn':
			return 4.51*shaft.Sut**-0.265
		elif shaft.finish == 'hot-rolled':
			return 57.7*shaft.Sut**-0.718
		elif shaft.finish == 'as-forged':
			return 272*shaft.Sut**-0.995
		else:
			print('check surface finish please')
			
	def Kb(d):
		if d<=0.051:
			return 1.24*d**-0.107
		else:
			return 1.51*d**-0.157
			
	def Ke():
		return 1-.08*4.265 #99.999% reliability 1 in 100000 failure
		
	if shaft.Sut < 1400:
		SePrime = .5*shaft.Sut
	else:
		print('Tensile strength too high')
		
	Ka1 = Ka()
	Kb1 = Kb(shaft.d1)
	Kb2 = Kb(shaft.d2)
	Kb3 = Kb(shaft.d3)
	Ke1 = Ke()
	
	#select highest Kb
	if Kb1 > Kb2 and Kb1 > Kb3:
		kb = Kb1
	elif Kb2 > Kb1 and Kb2 > Kb3:
		kb = Kb2
	else:
		kb = Kb3
		
	Se = SePrime*Ka1*kb*Ke1
	
	return Se