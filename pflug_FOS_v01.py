import numpy as np

def fatigue(Se, sigmaA, tauM, shaft):

	Sut = shaft.Sut
	
	sigmaAprime = ((sigmaA)**2)**.5
	sigmaMprime = ((3*(tauM)**2))**.5
	
	n = (sigmaAprime/Se+sigmaMprime/Sut)**-1 #modified goodman
	
	return n
	
def static(sigma, tau, shaft):

	Sy = shaft.Sy

	def distEnergy(sigma, tau):
		#bending stress and torsion only
		sigmaPrime = (sigma**2+3*tau**2)**.5
		return sigmaPrime
		
	sigmaPrime = distEnergy(sigma, tau)
	
	n = Sy/sigmaPrime
	
	return n