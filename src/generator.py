import random, json

n = 50
branches = [(a, b) for a in range(n) for b in range(n) if a < b and random.random() < 0.25]
vertices = {}
for i in range(n):
	vertices[str(i)] = []

for (a, b) in branches:
	vertices[str(a)].append(str(b))

for i in range(15, 25):
	f = open("input" + str(i) + ".json" ,"w+")
	json.dump(vertices, f)
