# Charted-Particle-Velocity-Simulator
A small part of a greater project I am working on. This program uses a derived equation from Couloumb's Law to calculate the velocity of either an electron or a proton to a 1d charged bar.

The program can be split into three distinct parts:
  1: Force Build
    In this section of the program the code takes the parameters passed on by the selected parameter list for the chosen particle, and accuracy passed on by the user, to     calculate the force experienced by the particle at each distance from the bar, starting from 5m (the s parameter). This is done by a group of functions, one which       itterates over each value of distance, with a step given by the acceleration varuible, passing on each itteration value (distance value) to a nested function             'forceBuild' which completse the required integral for the corresponding force value using SciPy's quad. function. This value and the distance value are then             appended to a numpy array to be graphed using Matplotlib.
       Formula used for forceBuild:
       ![image](https://user-images.githubusercontent.com/51892128/202745923-9a644331-5edf-4f3e-a2e6-e7c93154f99d.png)

    
  2: Acceleration Build:
    In the second, and simplest section of the code the force values are passed onto the function 'accelerationBuild' to be divided by the m (mass) parameter, to solve       for the acceleration using F=ma. This itterated for every value of force array, and is then appended to a second acceleration numpy array which is then graphed.
       Formula Used for accelerationBuild:
       ![image](https://user-images.githubusercontent.com/51892128/202746154-f6389824-1557-4d7d-bc5b-01cac09adfcb.png)
    
  3: Velocity Build
    The third, and most complex part of the code is the velocity transform. The reason for this complexity is that for each velocity value, the velocity at the point       directly behind iteslf must be first calculated. Meaning that the function is self-refferential, this just requires us to use a summation within our function which       calculates the velcocity for every point before itself using an accuracy of n (step number). This summation is coded using a a variety of functions. First itterating     over each value of distance (to the accuracy outlined by the accuracyVar), which is passed onto a summation coded using a simple for loop which a range of the           difference between the summation limits, which applies and summates the sumamtion equation until satisfying the range. It then appends the result to a numpy array, and   continues with the next value of d until all over itterated over. Then finally graphing using matplotlib.
     Formula used for velocityBuild:
     ![image](https://user-images.githubusercontent.com/51892128/202746834-c4d92199-47d4-4332-bb2a-cd7e83bb455e.png)
    
The program then spits out the final velocity, graphs for each section, and some information about the computational time.

NOTE: There is a main problem within the accuracy of the code, that being the value of the second charge particle being hard-coded as a random small number. I am currenly working on an equation to derive the proper value, though doing so requires solving a rather gross riemann sum... So it may take a while.
