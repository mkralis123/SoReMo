import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency
import matplotlib.pyplot as plt

year = 2020

table = pd.read_csv("AlgStatsData/" + str(year) + "TwoWayTable.csv")
table = np.delete(table.values, [0], axis = 1).astype(int)

with open('BasesFunctions.txt') as f:
    lines = f.readlines()
    
    
bases = []

for i in range(len(lines)):
    
    if i%3==0:
        if 't' in lines[i]:    
            continue
        else:    
            bases.append((lines[i].split("âˆ’")[0].split('x')[1],
                          lines[i].split("âˆ’")[0].split('x')[2],
                          lines[i].split("âˆ’")[1][0:-1].split("x")[1],
                          lines[i].split("âˆ’")[1][0:-1].split("x")[2]))
          
            
markovBases = []
            
for i in range(len(bases)):
    
    temp = np.zeros((16,))
    
    for j in range(4):
        
        if j <2:
            temp[int(bases[i][j])-1] = 1
        else:
            temp[int(bases[i][j])-1] = -1
        
        
    markovBases.append(temp.reshape((4,4)).astype(int))
    
    
    
def getPVal(histogram, chiSquare):
    
    pVal = 0
    for i in range(len(histogram)):
        
        if chiSquare < histogram[i]:
            
            pVal +=1
            
    pVal = pVal/len(histogram)
    
    return pVal
    
    
    
def runMonteCarlo(table,markovBases, N):
    
    M = len(markovBases)
    baseChiSquare = chi2_contingency(table)[0]
    
    ChiSquares = []
    moves = []
    signs = []
    
    pVals = []
    numPvals = 0
    
    for i in range(N):
        
        sign = np.random.randint(2)
        n = np.random.randint(M)
        
        if sign == 1:
            basis = markovBases[n]

        else:
            basis = -markovBases[n]

        
        if np.any(table + basis < 0):
            
            continue
        
        else:
            moves.append(n)
            
            if sign == 1:
                signs.append(1)
            else:
                signs.append(-1)
            
            table = table + basis

        ChiSquares.append(chi2_contingency(table)[0])
        
        if baseChiSquare < ChiSquares[-1]:
            numPvals += 1
            
        pVals.append(numPvals/(i+1))
    
    return ChiSquares, baseChiSquare, moves,signs, pVals, table


histogram, chiSquare, moves,signs, pVals, newtable = runMonteCarlo(table,markovBases,100000)
        
        
plt.hist(moves, bins = 36)
plt.show()
        
plt.hist(histogram, bins = 50)
plt.axvline(x=chiSquare, color='k', label='Base Chi Square')
plt.legend()
plt.show()


plt.plot(pVals)
plt.title("P-Value by Steps")
plt.xlabel("Steps")
plt.ylabel('P-Value')
plt.show()


# for i in range(len(moves)):
    
#     table = table + signs[i]*markovBases[moves[i]]