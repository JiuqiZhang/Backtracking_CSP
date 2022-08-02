#Jiuqi Zhang
#Artificial Intelligence 
#CS 4613 Fall 2021
#Project 2: Map Coloring
import copy
FAILURE = -97



#This sets up the attributes for every spot on the map 
#SPOT struct
class SPOT:
    def __init__(self, variable, colors):
        self.name = variable
        self.neighbor = []
        self.is_signed = False
        self.color = False
        self.color_selection = copy.deepcopy(colors)


#This is the CSP class, which holds the domain, variables, and constraints
class CSP:
    def __init__(self,lines):
        self.variables = lines[1].split()
        self.domain = lines[2].split()
        self.constraints = lines[3:]
        self.var_num = int(lines[0].split()[0])







#This is the function that reads the input file
def readFile(filename):
    f = open(filename)
    lines = f.readlines()
    
    #close the file after reading
    f.close()       

    #initiate the CSP class
    csp = CSP(lines)
    csp.constraints = [constraint.split() for constraint in csp.constraints]    #split the constaints to make them a list

    #initiate with SPOT class
    for i in range (len(csp.variables)):
        csp.variables[i] = SPOT(csp.variables[i], csp.domain)


    

    #read the constraints and collect neighbors info and save them into SPOT attibute
    for i in range(csp.var_num):
        for j in range(len(csp.constraints[i])):
            if (csp.constraints[i][j] == '1'):
                csp.variables[i].neighbor.append(csp.variables[j].name)
                


    
    #geneerate output which contains N lines for N variables
    for assignment in backTrackingSearch(csp):
        print(assignment)

    return



#select the spot with least legal value selection
def MRV_heuristic(csp):
    ret = []
 
    least = None
    for spot in csp.variables:
        if (spot.is_signed == False):
            if (least == None):
                least = spot
                mini = len(spot.color_selection)
                
            if len(spot.color_selection) <= mini:
                least = spot
                mini = len(spot.color_selection)
                ret.append(len(spot.color_selection))

    ret.sort()
    if len(ret) > 1:
        if (ret[0] == ret[1]):
            return False
    return least


#select the spot with most unsigned neighbor
def degree_heuristic(csp):
    repli = copy.deepcopy(csp)
    stat = []
    unsigned = []
    for spot in csp.variables:
        if spot.is_signed == False:
            unsigned.append(spot.name)

    for i in range(repli.var_num):                  #loop the index for each variable
        unsigned_neighbor = 0
        for neighbor in repli.variables[i].neighbor:#loop the neighbors of each variable
            if neighbor in unsigned:
                unsigned_neighbor += 1                    
        if (repli.variables[i].is_signed == True):
            stat.append(-1)
        else:
            stat.append(unsigned_neighbor)
        #print(repli.variables[i].name+' has unsigned neighbors of ', unsigned_neighbor)
    max = stat[0]
    max_ind = 0
    for i in range(len(stat)):
        if stat[i] > max:
            max = stat[i]
            max_ind = i             #holds which one has the most unsigned neighbor
    stat.sort()
    if stat[-1] == stat[-2]:           #if more than 1 choice, return false
        return False
    return csp.variables[max_ind]

    




#select next variable using MRV and degree heuristic functions
def selectUnsignedVariable(csp):
    if (MRV_heuristic(csp) == False):                           #MRV not found go degree
        if (degree_heuristic(csp) == False):                    #dgree not found return random one (arbitrarily based on input order)
            for spot in csp.variables:
                if spot.is_signed == False:
                    return spot
            
        return degree_heuristic(csp)                            #degree found, return selected
    return MRV_heuristic(csp)                                   #MRV found, return selected




#forward checking
#update domain of its neighbors, return false if neighbors got no colorselections left
def Inference(csp, spotName, color):
    repli = copy.deepcopy(csp)                              #deep copy so it won't affect the original csp when updating other's domain

    for neighbor in repli.variables:
        if (spotName in neighbor.neighbor):

            #when the neighbor is not signed
                                                                                            #print(neighbor.name, neighbor.is_signed, neighbor.color_selection)
            if (neighbor.is_signed == False):
                                                                                            #print(neighbor.name, ' : ', neighbor.color_selection)
                #update the neighbors' domain
                if color in neighbor.color_selection:                       #
                    neighbor.color_selection.remove(color)

                                                                                            #print(neighbor.name, ' : ', neighbor.color_selection)
                if neighbor.color_selection == []:
                                                                                            #print('wrong way!!!!!!!!!!!!! run out of ', neighbor.name)
                    return FAILURE
                    #when the domain is empty, it means it fails.
    for spots in repli.variables:
        if spots.name == spotName:
                                                                                            #print('?????????????????????? did I sign?', spots.name)
            spots.is_signed =True
            spots.color = color
    return repli


     
#the following are the implemented backTracking algorithm (given pseudo code)   
def backTrackingSearch(csp):
    return backTrack(csp, [])

def backTrack(csp, assignment):
                                                                                                                #print(assignment)

    if (len(assignment) == csp.var_num):
        return assignment
    spot = selectUnsignedVariable(csp)                                      #remember to update the spot!!!!!!!
                                                                                                                #print(spot.is_signed)
    for i in range(csp.var_num):
        if csp.variables[i].name == spot.name:
            break
                                                                                                                #print(csp.variables[i].color_selection)
    for color in csp.variables[i].color_selection:
        assignment.append(spot.name+' = '+ color)
                                                                                                                #print(csp.variables[i].name+' = '+ color)

        inference = Inference(csp, csp.variables[i].name, color)

        if (inference != FAILURE):
            result = backTrack(inference, assignment)
            if (result != FAILURE):
                return result
        assignment.pop()   
                                                                                                                #print("Didn't workout")         
    return FAILURE        
    


        



def main():
    #to save your time
    #readFile(input("\nInput the file name please(e.g. 'Input1.txt'):\n"))

    readFile('Input1.txt')
main()