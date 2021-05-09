import matplotlib.pyplot as plt
import json

files = [
  'morts.json',
  'morts_par_espece.json',
  'naissance.json'
]

for i in files:
  file = open(i, 'r')
  content = json.loads(file.read())
  file.close()
  plt.bar(range(len(content)),[ content[i] for i in content.keys()])
  plt.xticks(range(len(content)), list(content.keys()))
  plt.title(i)
  plt.show()

file = open('age.json', 'r')
content = json.loads(file.read())
file.close()
liste = {}
for i in content.keys():
  x = 0
  for j in content[i]:
    x += content[i][j]
  liste[i] = x/len(content[i])
plt.bar(range(len(liste)),[ liste[i] for i in content.keys()])
plt.xticks(range(len(liste)), list(liste.keys()))
plt.title('age.json')
plt.show()
  