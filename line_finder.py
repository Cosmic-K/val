#Name: Krishna Mooroogen
#Date: 15/06/19
#Last update: 16/06/19
#Description: 
#  Line finder code - valerann
#  short bit of code to arbitrarily find 
#  straight lines (individual moving objects) in time-distance data 

#module imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math


def hugh(data) :
#Hough Transform version
#where rho is the distance from the origin to the 'line'
#theta is the angle between the axis and rho 
#where theta and rho are the same for a x,y pair the coordinate should lie on the line
#algortihm to store all rho and thetas for each xy pair

	#accumaltor array stores rho and theta that satisfy equation
	#706 as longest diagnal lenght for 499x499 space
	#180 degrees for high resolution angle 
	#498
	acc=np.zeros((706,181),dtype=np.float)

	#xy_=np.empty(498,dtype=np.float)
	#rho_=np.empty(706,dtype=np.float)
	#theta_=np.empty(181,dtype=np.float)

	for i, (x, y) in enumerate(zip(data['T'],data['x'])):
		#loop over xy 
		for  rho in range(706):	
			#loop over all rho
			for theta in range(0,181):
				#loop over all angles
				if (rho==y*math.cos(theta*math.pi/180) + x*math.sin(theta*math.pi/180)):
		
					#for Debugging
					#xy_=np.append(xy_,[i])
					#rho_=np.append(rho_,[rho])
					#theta_=np.append(theta_,[theta]) 
					#print(i,rho,theta)
					
					#voting: add ones to positions where rho and theta are same 
					#To do: keep track of xy index for each theta, rho
					#figure out the parameter space
					acc[rho][theta]+=1
					

	return(acc) 



def linear_finder(data): 
		#linear version of line finder using a gradient match method
		#calculate all possible gradients for a single point given a limited set of intercepts
		#To do: search over gradients for a partciular intecept over all points, 
		#points which have same gradient (close to) and intercept sit on same line

		m=np.zeros((498),dtype=np.float)
		#array shaped by number of points and number of intercepts
		#intercept values may not be physical considering the graph

		#loop over x & y
		for i, (x, y) in enumerate(zip(data['T'],data['x'])):

			#calculate gradient from list of intercepts
			#for c in range(172):
			m[i]=((y)/x)	


		return(m)


def finder():
	#main calling program

	#change time to to minutes for ease of plotting and math
	#read data in 

	df=pd.read_csv('data.csv')
	time=pd.DatetimeIndex(df['T'])
	T=time.hour*60+time.minute+time.second/60.
	df['T']=T

	#plot data
	plt.plot(df['T'],df['x'],'.')

	#call hugh method and inspect 
	acc = hugh(df)
	#inspect rho and theta votes
	nz=np.nonzero(acc)
	nz_row=nz[0]
	nz_col=nz[1]
	for row, col, in zip(nz_row,nz_col):
		print('acc[{},{}]={}'.format(row,col,acc[row,col]))

	#call linear method
	#need to write search algo	
	m=linear_finder(df)


	return (m)