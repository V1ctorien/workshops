import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from apyori import apriori

store_data = pd.read_csv(r'C:\Users\victorien.sauvonnet\Documents\ma_formation\mes_projets\apriori\data\store_data.csv', header=None) # header none  supprime l'entete 
record= []
for i in range(0, 7501):
    record.append([str(store_data.values[i,j]) for j in range(0, 20)])  #cree une liste de liste 20colonnes 7501 ligne
association_rules = apriori(record, min_support=0.0045, min_confidence=0.2, min_lift=3, min_length=2)# creations de rules avec apriori 
association_results = list(association_rules)# mise en liste
print(len(association_results))
print(association_results[0])

for item in association_results:

    # first index of the inner list
    # Contains base item and add item
    pair = item[0] 
    items = [x for x in pair]
    print("Rule: " + items[0] + " -> " + items[1])

    #second index of the inner list
    print("Support: " + str(item[1]))

    #third index of the list located at 0th
    #of the third index of the inner list

    print("Confidence: " + str(item[2][0][2])) #pour chaque entrer de association_results recup dans la liste d'index 2 l'index 2 de l'index 0) 
    print("Lift: " + str(item[2][0][3]))
    print("=====================================")