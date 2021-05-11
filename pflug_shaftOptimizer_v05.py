import numpy as np
import matplotlib.pyplot as pl
import pflug_beamObj_v02 as beam
import scipy.optimize
import pflug_staticStress_v03 as statStress
import pflug_FOS_v01 as FOS
import pflug_fatigueStrength_v01 as fs

shaft = beam.beam()
	
#change shaft variables here
shaft.d1 = .045
shaft.d2 = .07
shaft.d3 = .045 
	
shaft.r12 = .007
shaft.r23 = .007

shaft.Sut = 690
shaft.Sy = 580

shaft.finish = 'cold-drawn'

def stress(M,d):
	c = (d)/2
	I = (np.pi/64)*(d)**4
	return (M*c)/I

def momentPlot(x,y):
	
	fig = pl.figure(figsize=(8,6))
	ax = fig.add_subplot(1,1,1)
	ax.plot(x,y)
	
def residual(vars):

	N = 1.5 #FOS
	
	shaft.d1 = vars[2]-vars[0]*vars[3] #updates the value of d1 based on q1
	shaft.d2 = vars[2]
	shaft.d3 = vars[2]-vars[1]*vars[4] #updates the value of d3 based on q2
	
	shaft.r12 = vars[3]
	shaft.r23 = vars[4]
	
	Se = fs.fatigueStrength(shaft)
	sigma, tau = statStress.shoulderStresses(shaft)
	
	n = FOS.fatigue(Se, sigma, tau, shaft)
	V = shaft.volume()
	
	R = np.linalg.norm(np.array([N-n, V]))
	
	if shaft.d2/shaft.d1 < 1.15 or shaft.d2/shaft.d3 < 1.15:
		R += 10
	
	return R
	
def main():
	
	#for expressing d1 and d2 in terms of h/r
	h1 = shaft.d2-shaft.d1
	h2 = shaft.d2-shaft.d3
	q1 = h1/shaft.r12
	q2 = h2/shaft.r23
	
	vars = np.array([q1, q2, shaft.d2, shaft.r12, shaft.r23]) #free variables
	bnds = ((.25,4),(.25,4),(0,None),(0,None),(0,None)) #bounds
	
	sol = scipy.optimize.minimize(residual, vars, method = 'L-BFGS-B', bounds=bnds, tol=1e-3)
	
	print('Diameter 1: ' + str(shaft.d1) + ' m')
	print('Diameter 2: ' + str(shaft.d2) + ' m')
	print('Diameter 3: ' + str(shaft.d3) + ' m')
	print('radius 12: ' + str(shaft.r12) + ' m')
	print('radius 23: ' + str(shaft.r23) + ' m')
	print('length 1: ' + str(shaft.L1) + ' m')
	print('length 2: ' + str(shaft.L2) + ' m')
	print('length 3: ' + str(shaft.L3) + ' m')
	print('mass: ' + str(shaft.volume()*shaft.density) + ' kg')
	
	Se = fs.fatigueStrength(shaft)
	sigma, tau = statStress.shoulderStresses(shaft)
	
	print('Fatigue FOS: ' + str(FOS.fatigue(Se, sigma, tau, shaft)))
	print('Yield FOS: ' + str(FOS.static(sigma, tau, shaft)))
	
	  #Moment diagram
	x = np.linspace(0,shaft.L1+shaft.L2+shaft.L3-.01,100)
	y = np.zeros(x.size)
	for i in range(x.size):
		y[i] = shaft.moment(x[i])
	momentPlot(x,y)
	pl.show()

if __name__=='__main__': main()