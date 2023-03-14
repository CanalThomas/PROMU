import json
import matplotlib.pyplot as plt

with open("X.json", "r") as f:
    X = json.load(f)

with open("Y.json", "r") as g:
    Y = json.load(g)

# fig, ax = plt.subplots()
# ax.set_xlim(0, 128)
# ax.set_ylim(0, 128)
# ax.scatter(X, Y)
# fig.show()

X, Y = [62, 99, 21, 95], [35, 71, 66, 71]

plt.scatter(X, Y)
plt.xlim(0, 128)
plt.ylim(0, 128)
plt.show()