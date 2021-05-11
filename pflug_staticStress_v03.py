import numpy as np

def shoulderStresses(shaft):
	
	def bendingConcFactor(d1, d2, r):
		#calculates bending stress concentration
		h = np.abs(d1-d2)
		
		if d1/d2 < 1:
			d = d1
			D = d2
		elif d1/d2 > 1:
			d = d2
			D = d1
		else:
			return 1
			
		if .25<=h/r and h/r <= 2.0:
			c1 = .927+1.149*(h/r)**.5-.086*h/r
			c2 = .015-3.281*(h/r)**.5+.837*h/r
			c3 = 0.847+1.716*(h/r)**.5-0.506*h/r
			c4 =-.790+0.417*(h/r)**.5-.246*h/r
		elif h/r <= 20:
			c1 = 1.225+.831*(h/r)**.5-.010*h/r
			c2 = -3.790+.958*(h/r)**.5-.257*h/r
			c3 = 7.374-4.834*(h/r)**.5+.862*h/r
			c4 = -3.809+3.046*(h/r)**.5-.595*h/r
		else:
			print(h/r)
			print("h/r out of range, bending")
			
		Kt = c1 + c2*(2*h/D)+c3*(2*h/D)**2+c4*(2*h/D)**3
		
		return Kt
		
	def torsionConcFactor(d1, d2, r):
		#calculates torsion stress concentration factor
		h = np.abs(d1-d2)
		
		if d1/d2 < 1:
			d = d1
			D = d2
		elif d1/d2 > 1:
			d = d2
			D = d1
		else:
			return 1
			
		if .25<=h/r and h/r <= 4.0:
			c1 = .958+0.680*(h/r)**.5-.053*h/r
			c2 = -.493-1.820*(h/r)**.5+.517*h/r
			c3 = 1.621+0.908*(h/r)**.5-0.529*h/r
			c4 =-1.081+0.232*(h/r)**.5+.065*h/r
		else:
			print(h/r)
			print("h/r out of range, torsion")
			
		Kt = c1 + c2*(2*h/D)+c3*(2*h/D)**2+c4*(2*h/D)**3
		
		return Kt
		
	def distEnergy(sigma, tau):
		#bending stress and torsion only
		sigmaPrime = (sigma**2+3*tau**2)**.5
		return sigmaPrime
		
	#assumes peak stress will occur at one of the shoulders
	d1 = shaft.d1
	d3 = shaft.d3
	I1 = np.pi*d1**4/64
	I3 = np.pi*d3**4/64
	
	#calculate torsion and bending stress concentration factors
	Ktbend1 = bendingConcFactor(d1, shaft.d2, shaft.r12)
	Ktbend2 = bendingConcFactor(d3, shaft.d2, shaft.r23)
	Kttors1 = torsionConcFactor(d1, shaft.d2, shaft.r12)
	Kttors2 = torsionConcFactor(d3, shaft.d2, shaft.r23)
	
	#calculate torsion and bending stresses
	sigma1 = Ktbend1*shaft.moment(shaft.L1)*d1*.5/I1*1E-6
	sigma2 = Ktbend2*shaft.moment(shaft.L1+shaft.L2)*d3*.5/I3*1E-6
	tau1 = Kttors1*shaft.torque(shaft.L1)*d1/I1*1E-6
	tau2 = Kttors2*shaft.torque(shaft.L1 + shaft.L2)*d3/I3*1E-6
	
	#calculate sigma prime with distortion energy at each shoulder
	sigmaPrime1 = distEnergy(sigma1, tau1)
	#print('Shoulder 1: ' + str(sigmaPrime1) + " MPa")
	sigmaPrime2 = distEnergy(sigma2, tau2)
	#print('Shoulder 2: ' + str(sigmaPrime2) + " MPa")
	
	if sigmaPrime1 >= sigmaPrime2:
		return sigma1, tau1
	else:
		return sigma2, tau2