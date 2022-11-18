# logistical
import math
from numpy import exp
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
import time
from statistics import mean
# user-end
from alive_progress import alive_bar
from colorama import Fore
from colorama import Style
import matplotlib as mpl
mpl.rcParams["mathtext.fontset"]='cm' #Changes math font to Computer Modern

# Improvements over V1:
    # Plotting function universal for multiple displays
    # Nested functions in order to differentiate graph calls
    # Returns percentage over c in error message
    # Returns Processing info
    # More accurate calculation for velocity
    # A final velocity message, with % of c
    # Colored Text
    # Progress bars for each calculation

# Notes:
    # PROBLEM: Ciel. Func in summation()
    # ACCURACY: Loretnz Factor
    # ERROR: force experienced over-estimated(?)
    # Check if effect is repulsive or attractive
    # subplot that bih

computationsNum = [0, 0, 0]
absErr = []
# Varuible Lists
print('which varuible type would you like to use?\n1 = Test\n2 = Actual - Proton\n3 = Actual - Electron')
var_type = input()
print('Please print the level of accuracy at which you would like to calculate with.\n   0.01 is reccomended for quick tests\n   0.001 is reccomended for more thurough tests ~3 minutes computational time\n   anything lower than 0.0001 will take over ten minutes to compute.')
accuracyVar = float(input())
# Format: variubles = [h, s, m, q1, q2, k, n, d-step]
if var_type == '1': #Test
    varuibles = [3, 5, 0.001, 1, 5, 0.1, accuracyVar, accuracyVar] 
    particle = (' Test')
elif var_type == '2': #Actual - Proton  
    varuibles = [0.1, 5, (1.67262192*10**-27), (1.6*10**-19), 0.0001, (8.9875517923*10**9), accuracyVar, accuracyVar] 
    particle = (' Proton')
elif var_type == '3': #Actual - Electron
    varuibles = [0.1, 5, (9.1093837*10**-31), (-1.6*10**-19), 0.000000001, (8.9875517923*10**9), accuracyVar, accuracyVar]
    particle = ('n Electron')
# Varuibles:
computationsNum = [0, 0, '', ''] #stores [0]: integral calculations, [1]: linear caclulations, [2]: time start, [3]: time end
computationsNum[2] = time.time()
h = varuibles[0]   # Height of charged bar (m)
s = varuibles[1]   # Point at which Vi = 0 (m)
m = varuibles[2]   # Mass of particle(kg)
q1 = varuibles[3]   # Charge 1 (C)
q2 = varuibles[4]   # Charge 2 (C)
k = varuibles[5]   # Couloumbs Constant
n = varuibles[6]   # Step Number (approaches zero)
step = varuibles[7]   # step accuracy of d during plotting


def distanceItteration(func): # Itterates over values of d for specified function, returns numpy array
    graphX = []
    graphY = []
    # Assumes only use of distanceItteration is forceBuild
    print('Force Build Time:')
    with alive_bar(math.ceil(s/step)) as bar:
        for x in reversed(np.arange(0, s, step)): #itterates over each value of d
            y = func(x) 
            graphX.append(x) 
            graphY.append(y)
            bar()
    x_values = np.array(graphX)
    y_values = np.array(graphY)
    return x_values, y_values

def graphingFunc(x_values, y_values, pltType): # Returns plotted graph, provided plot type and coordinate values
    def plot(x_values, y_values, pltType): # Plots given points, with specified Type and array(s)
        plt.style.use('seaborn-darkgrid')
        # plt.figure(pltType)
        # Checks graph type, adds proper attributes
        plt.suptitle('Effect of an Electric Field on a'+particle, fontsize=20)
        if pltType == 'f(d)':
            plt.subplot(1, 3, 3)
            plt.title('Force(distance)', fontsize=15, y=1.03)
            plt.ylabel('Force (N)')
            lineColor = 'r'
            plt.xlabel('Distance (m)')
            plt.figtext(0.72, 0.04, r'$f(d) = \int_{d}^\sqrt{(d)^2+(h/2)^2}\frac{d}{r}\cdot k \frac{\vert q_1 q_2 \vert}{r^2} dr$', multialignment='left', fontsize=10, bbox={"facecolor":"red", "alpha":0.3, "pad":6})
        if pltType == 'a(d)':
            plt.subplot(1, 3, 2)
            plt.xlabel('Distance (m)')
            plt.title('Acceleration(distance)', fontsize=15, y=1.03)
            plt.ylabel('Acceleration (m/'+r'$s^2$'+')')
            plt.figtext(0.455, 0.032, r'$a(d) = \frac{\int_{d}^\sqrt{(d)^2+(h/2)^2}\frac{d}{r}\cdot k \frac{\vert q_1 q_2 \vert}{r^2} dr }{m}$', multialignment="left", fontsize=10, bbox={"facecolor":"blue", "alpha":0.3, "pad":7})
            lineColor = 'b'
        if pltType == 'v(d)':
            plt.subplot(1, 3, 1)
            plt.xlabel('Distance (m)')
            lineColor = 'g'
            plt.title('Velocity(distance)', fontsize=15, y=1.03)
            plt.ylabel('Velocity (m/s)')
            plt.figtext(0.181, 0.04, r'$v(d) = \sqrt{\sum_{x=0}^{\frac{s-d}{n}-1} 2a(d-xn)n}$', multialignment="left", fontsize=10, bbox={"facecolor":"green", "alpha":0.3, "pad":5})
            cPerc = math.ceil((y_values[-1]/299792458)*100)
            print(f'\n{Fore.RED}Velocity at d -> 0:', str("{:,}".format(math.ceil(y_values[-1])))+'m/s -', str(cPerc)+'% speed of light') #%s kinda funky
            if y_values[-1] >= 299792458:  
                cPerc = math.ceil(((y_values[-1]-299792458)/299792458)*100)
                plt.suptitle('VALUE_ERROR: Final Velcity Exceeds Speed of Light by: '+str("{:,}".format(y_values[-1]-299792458))+'m/s - '+str(cPerc)+'%', fontsize=7, color='r')
        plt.subplots_adjust(bottom=0.15)
        plt.plot(x_values, y_values, marker=',', mfc='r', color=lineColor)
        return

    # Calling Functions
    plot(x_values, y_values, pltType)
    return x, y

# Force-Distance Build
def forceBuild(d): # Returns Force Array, provided Distance(d)        
    def forceEqn(r, d): #Equation for Integration
        # function f(d)
        x = 2*((d/r)*(k*((abs(q1*(q2/h)))/r**2)))
        computationsNum[0] = computationsNum[0]+1
        return x

    def forceIntgrl(d):  #Itegration of Force Equation
        limUpper = (math.sqrt(((d)**2)+((h/2)**2)))
        computationsNum[0] = computationsNum[0]+1
        # integration over r
        i, err = quad(forceEqn, d, limUpper, args=(d))
        absErr.append(err)
        computationsNum[1] = computationsNum[1]+1
        return(i)

    # Calling Functions
    forceExperienced = forceIntgrl(d)
    return forceExperienced

# # Acceleration-Distance Build
def accelerationBuild(forceArray): # Returns acceleration value array, provided force array
    def acceleration(forceArray): 
        # f(d) -> a(d)
        accelerationArray = []
        print('Acceleration Build Time:')
        with alive_bar(len(forceArray)) as bar:
            for x in forceArray:
                accelerationArray.append(x/m)
                computationsNum[0] = computationsNum[0]+1
                bar()
        return accelerationArray
    
    # Calling Functions
    accelerationExperienced = acceleration(forceArray)
    return accelerationExperienced
# Velocity Distance Build
def velocityBuild(x_values, accelerationArray): # Returns velocity experienced, provided distance
    def velocity(x_values, accelerationArray):
        velocityArray = []
        print('Velocity Build Time:')
        with alive_bar(len(x_values)) as bar:
            for x in x_values:
                # Distance must be divisible by n
                limUpper = ((s-x)/n)
                computationsNum[0] = computationsNum[0]+1
                sum = summation(limUpper, 0, accelerationArray)
                sum = math.sqrt(sum)
                computationsNum[0] = computationsNum[0]+1
                velocityArray.append(sum)   
                bar()
        return velocityArray
    # Calling Functions
    velocityArray = velocity(x_values, accelerationArray)
    return velocityArray

# Summation Func
def summation(limUpper, limLower, accelerationArray): # Returns sum total, provided limits
    def summation(limUpper, limLower, acclerationArray): #summation in loop form
        sum = 0
        # PROBLEM: Ceil func
        itterations = math.ceil(limUpper-limLower)
        computationsNum[0] = computationsNum[0]+1
        for x in range(0, itterations):
            sum = sum+sumFunc(x, acclerationArray)
            computationsNum[0] = computationsNum[0]+1
            # incorrect order - low dist = high itterate, not inverse
        return sum

    def sumFunc(x, accelerationArray): #function for summation
        index = round(s-x*n, len(str(step).split(".")[1]))
        index = int(index*(10**(len(str(step).split(".")[1]))))
        a = accelerationArray[-index]
        # acceleration index was hitting inverse indicies, negitive is a band-aid fix
        x = (2*a*n)
        computationsNum[0] = computationsNum[0]+3
        return x
    
    # Calling Functions
    sumTotal = summation(limUpper, limLower, accelerationArray)
    return sumTotal

def processingInfo(computationsNum):
    computationsNum[3] = time.time()
    timeElapsed = round(computationsNum[3]-computationsNum[2], 2)
    print(f'{Fore.GREEN}Processing Info:{Style.RESET_ALL}')
    print('   Time Elapsed:', str(timeElapsed)+' seconds')
    print('   Average Absolute Error:', '('+str(((mean(absErr))*100))+')%')
    print('   Total Integral Computations:', ("{:,}".format(computationsNum[1])))
    print('   Total Linear Computations:', ("{:,}".format(computationsNum[0])))

x, y = distanceItteration(forceBuild)
graphingFunc(x, y, 'f(d)')
y = accelerationBuild(y)
graphingFunc(x, y, 'a(d)')
y = velocityBuild(x, y)
graphingFunc(x, y, 'v(d)')
processingInfo(computationsNum)
plt.show()

