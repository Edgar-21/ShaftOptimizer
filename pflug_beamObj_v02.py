import numpy as np

class beam:

	def __init__(self):
		
		#all in meters
		
		#bearing widths
		self.b1width = .017
		self.b2width = .023
		
		#gear width
		self.Gwidth = .025
		
		#lengths of each diameter section
		self.L1 = .08+.5*self.Gwidth+.5*self.b1width
		self.L2 = .3-.5*self.Gwidth-.5*self.b2width
		self.L3 = .08+.5*self.b2width+.5*self.Gwidth
		
		#diameters
		self.d1 = .035
		self.d2 = .075 #bearing table suggests .074, does not meet design requirement, however
		self.d3 = .065
		
		#fillet radii
		self.r12 = .003 #variable, this transition is near the gear
		self.r23 = .003 
		
		#reactions in bearing a
		self.Fay = 1026.32
		self.Faz = -3217.11
		
		#reactions in bearing c
		self.Fcy = 4073.68
		self.Fcz = 7692.11
		
		#Material Properties
		self.Sut = 630
		self.Sy = 530
		self.finish = 'ground'
		self.density = 7870 #kg/m3
		
		
	def moment(self, x):
		
		#combines bending moment singularity equations as vectors and returns the magnitude at given x
		if x <= self.L1:
			M = ((self.Fay*x)**2+(self.Faz*x)**2)**.5
		elif x <= self.L1+self.L2:
			M = ((self.Fay*x-3600*(x-.08))**2+((self.Faz*x-1100*(x-.08))**2))**.5
		elif x <= self.L1+self.L2+self.L3:
			M = ((self.Fay*x-3600*(x-.08)+self.Fcy*(x-.38))**2+(self.Faz*x-1100*(x-.08)+self.Fcz*(x-.38))**2)**.5
		
		return M
		
	def torque(self, x):
		
		if x <= .08:
			T = 0
		else:
			T = 675
		return T
		
	def volume(self):
		V = (self.d1/2)**2*np.pi*self.L1+(self.d2/2)**2*np.pi*self.L2+(self.d3/2)**2*np.pi*self.L3
		return V
		
