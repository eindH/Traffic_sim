import time
import random
import tkinter

class TrafficLight:
    '''class to describe state of traffic light
    state = colour of light
    0 = red
    1 = red/orange
    2 = green
    3 = orange'''
    listOfStates = ['red', 'red/amber', 'green', 'amber']
    def __init__(self, state = 0):
        '''set all new lights to be red by default'''
        self.state = 0 #state    #colour of light
        self.carsBehind = 0    #cars waiting for light

class Entrance:
    '''class to describe an entrance to the roundabout'''
    def __init__(self, noOfLights : int):
        '''sets number of lights starting from left to right € {1, 2, 3}'''
        self.lights = []    #list of lights at entrance
        for i in range(noOfLights):
            self.lights.append(TrafficLight())
        
class Roundabout:
    '''class to model the roundabout
    The lights may allow cars to turn left; go straight and turn left; turn right, go straight and turn left or turn right
    Lights will change based on longest queue at the entrances'''
    def __init__(self):
        '''define light of entrances to roundabout N0, E1, S2, W3'''
        self.lights = [Entrance(3), Entrance(2), Entrance(3), Entrance(2)]    #list of entrances to roundabout
        self.state = 'NULL'
    
    def goToNull(self):
        '''set all lights to red for next state'''
        for i in range(len(self.lights)):    #check for green lights and turn to amber
            for j in range(len(self.lights[i].lights)):
                if self.lights[i].lights[j].state == 2:
                    self.lights[i].lights[j].state = 3
        time.sleep(1)
        for i in range(len(self.lights)):    #check for amber and turn to red
            for j in range(len(self.lights[i].lights)):
                if self.lights[i].lights[j].state == 3:
                    self.lights[i].lights[j].state = 0
    
    def transition(self, toState):
        '''transition junction lights to specified states'''
        if toState == 0:
            #North and south left and stright
            #set north lights
            self.lights[0].lights[0].state = 1
            self.lights[0].lights[1].state = 1
            #set south lights
            self.lights[2].lights[0].state = 1
            self.lights[2].lights[1].state = 1
            time.sleep(1)
            #set north lights
            self.lights[0].lights[0].state = 2
            self.lights[0].lights[1].state = 2
            #set south lights
            self.lights[2].lights[0].state = 2
            self.lights[2].lights[1].state = 2
            self.state = 'state0'
            
        elif toState == 1:
            #East and west left and straight
            #set east lights
            self.lights[1].lights[0].state = 1
            #set west lights
            self.lights[3].lights[0].state = 1
            time.sleep(1)
            #set east lights
            self.lights[1].lights[0].state = 2
            #set west lights
            self.lights[3].lights[0].state = 2
            self.state = 'state1'
            
        elif toState == 2:
            #East right, north and south left
            #set north lights
            self.lights[0].lights[0].state = 1
            self.lights[2].lights[0].state = 1
            #set east lights
            self.lights[1].lights[1].state = 1
            time.sleep(1)
            #set north lights
            self.lights[0].lights[0].state = 2
            self.lights[2].lights[0].state = 2
            #set east lights
            self.lights[1].lights[1].state = 2
            self.state = 'state2'
        
        elif toState == 3:
            #West right, north and south left
            #set south lights
            self.lights[2].lights[0].state = 1
            self.lights[0].lights[0].state = 1
            #set west lights
            self.lights[3].lights[1].state = 1
            time.sleep(1)
            #set south lights
            self.lights[2].lights[0].state = 2
            self.lights[0].lights[0].state = 2
            #set west lights
            self.lights[3].lights[1].state = 2
            self.state = 'state3'
        
        elif toState == 4:
            #North all directions
            self.lights[0].lights[0].state = 1
            self.lights[0].lights[1].state = 1
            self.lights[0].lights[2].state = 1
            time.sleep(1)
            self.lights[0].lights[0].state = 2
            self.lights[0].lights[1].state = 2
            self.lights[0].lights[2].state = 2
            self.state = 'state4'
        
        elif toState == 5:
            #South all directions
            self.lights[2].lights[0].state = 1
            self.lights[2].lights[1].state = 1
            self.lights[2].lights[2].state = 1
            time.sleep(1)
            self.lights[2].lights[0].state = 2
            self.lights[2].lights[1].state = 2
            self.lights[2].lights[2].state = 2
            self.state = 'state5'
        
        elif toState == 6:
            #East all directions
            self.lights[1].lights[0].state = 1
            self.lights[1].lights[1].state = 1
            time.sleep(1)
            self.lights[1].lights[0].state = 2
            self.lights[1].lights[1].state = 2
            self.state = 'state6'
        
        elif toState == 7:
            #East all directions
            self.lights[3].lights[0].state = 1
            self.lights[3].lights[1].state = 1
            time.sleep(1)
            self.lights[3].lights[0].state = 2
            self.lights[3].lights[1].state = 2
            self.state = 'state7'

def add_cars(junction):
    '''add cars to queues behind lights'''
    randIndex1 = random.randint(0, len(junction.lights) - 1)
    randIndex2 = random.randint(0, len(junction.lights[randIndex1].lights) - 1)
    junction.lights[randIndex1].lights[randIndex2].carsBehind += 1
    return [randIndex1, randIndex2]

def check_q_lengths(junction):
    '''check lengths of all queues'''
    qLength = 0
    index1 = 0
    index2 = 0
    for i in range(len(junction.lights)):
        for j in range(len(junction.lights[i].lights)):
            if junction.lights[i].lights[j].carsBehind > qLength:
                qLength = junction.lights[i].lights[j].carsBehind
                index1 = i
                index2 = j
    return [index1, index2]

def subtract_cars(junction, sleepTime):
    '''allows cars to leave queues when lights are green'''
    time.sleep(sleepTime)
    if junction.state == 'state0':
        if junction.lights[0].lights[0].carsBehind > 0:
            junction.lights[0].lights[0].carsBehind -= 1
        if junction.lights[0].lights[1].carsBehind > 0:
            junction.lights[0].lights[1].carsBehind -= 1
        if junction.lights[2].lights[0].carsBehind > 0:
            junction.lights[2].lights[0].carsBehind -= 1
        if junction.lights[2].lights[1].carsBehind > 0:
            junction.lights[2].lights[1].carsBehind -= 1
    
    if junction.state == 'state1':
        if junction.lights[1].lights[0].carsBehind > 0:
            junction.lights[1].lights[0].carsBehind -= 1
        if junction.lights[3].lights[0].carsBehind > 0:
            junction.lights[3].lights[0].carsBehind -= 1
    
    if junction.state == 'state2':
        if junction.lights[0].lights[0].carsBehind > 0:
            junction.lights[0].lights[0].carsBehind -= 1
        if junction.lights[2].lights[0].carsBehind > 0:
            junction.lights[2].lights[0].carsBehind -= 1
        if junction.lights[1].lights[1].carsBehind > 0:
            junction.lights[1].lights[1].carsBehind -= 1
    
    if junction.state == 'state3':
        if junction.lights[2].lights[0].carsBehind > 0:
            junction.lights[2].lights[0].carsBehind -= 1
        if junction.lights[0].lights[0].carsBehind > 0:
            junction.lights[0].lights[0].carsBehind -= 1
        if junction.lights[3].lights[1].carsBehind > 0:
            junction.lights[3].lights[1].carsBehind -= 1
            
    if junction.state == 'state4':
        if junction.lights[0].lights[0].carsBehind > 0:
            junction.lights[0].lights[0].carsBehind -= 1
        if junction.lights[0].lights[1].carsBehind > 0:
            junction.lights[0].lights[1].carsBehind -= 1
        if junction.lights[0].lights[2].carsBehind > 0:
            junction.lights[0].lights[2].carsBehind -= 1
    
    if junction.state == 'state5':
        if junction.lights[2].lights[0].carsBehind > 0:
            junction.lights[2].lights[0].carsBehind -= 1
        if junction.lights[2].lights[1].carsBehind > 0:
            junction.lights[2].lights[1].carsBehind -= 1
        if junction.lights[2].lights[2].carsBehind > 0:
            junction.lights[2].lights[2].carsBehind -= 1
            
    if junction.state == 'state6':
        if junction.lights[1].lights[0].carsBehind > 0:
            junction.lights[1].lights[0].carsBehind -= 1
        if junction.lights[1].lights[1].carsBehind > 0:
            junction.lights[1].lights[1].carsBehind -= 1
            
    if junction.state == 'state7':
        if junction.lights[3].lights[0].carsBehind > 0:
            junction.lights[3].lights[0].carsBehind -= 1
        if junction.lights[3].lights[1].carsBehind > 0:
            junction.lights[3].lights[1].carsBehind -= 1

def get_lenghts_of_queues(junction):
    '''get lengths of queues behind every traffic light and return a 2D list with them and sugested state'''
    queueLenghts = []
    queueLenghts.extend([[] for i in range(len(junction.lights))])
    carsForStates = []
    for i in range(len(junction.lights)):
        for j in range(len(junction.lights[i].lights)):
            queueLenghts[i].append(junction.lights[i].lights[j].carsBehind)
    
    carsForStates.append(queueLenghts[0][0] + queueLenghts[0][1] + queueLenghts[2][0] + queueLenghts[2][1]) 
    carsForStates.append(queueLenghts[1][0] + queueLenghts[3][0]) 
    carsForStates.append(queueLenghts[0][0] + queueLenghts[2][0] + queueLenghts[1][1])
    carsForStates.append(queueLenghts[2][0] + queueLenghts[0][0] + queueLenghts[3][1]) 
    carsForStates.append(queueLenghts[0][0] + queueLenghts[0][1] + queueLenghts[0][2]) 
    carsForStates.append(queueLenghts[2][0] + queueLenghts[2][1] + queueLenghts[2][2]) 
    carsForStates.append(queueLenghts[1][0] + queueLenghts[1][1]) 
    carsForStates.append(queueLenghts[3][0] + queueLenghts[3][1]) 
    stateToGoTo = 'state' + str(carsForStates.index(max(carsForStates)))
    return [queueLenghts, stateToGoTo]

def change_states(junction, stateToGoTo):
    junction.state = stateToGoTo

#Add cars to lanes randomly
#Choose which lights have most cars behind and see which state to switch to
#Subtract cars at a rate whilst still randomly adding to them
#Repeat step two

junction = Roundabout()

for i in range(500):
    add_cars(junction)

prevTime = int(time.time())
for i in range(1000):
    time.sleep(0.1)
    if int(time.time()) != prevTime or 1==1:
        add_cars(junction)
        junction.goToNull()
        change_states(junction, get_lenghts_of_queues(junction)[1])
        print(junction.state)
        subtract_cars(junction, 0)
        prevTime = int(time.time())