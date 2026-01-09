from sklearn.ensemble import BaggingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.datasets import load_digits
import matplotlib.pyplot as plt

bagging = BaggingClassifier(KNeighborsClassifier(), max_samples=0.5, max_features=0.5) # créé un bagging avec KNN

digits = load_digits() # charge le dataset des chiffres manuscrits

# Affichage des 10 premières images

fig = plt.figure()
for i, digit in enumerate(digits.images[:10]):
    fig.add_subplot(1,10,i+1)
    plt.imshow(digit)
plt.show()
