import matplotlib.pyplot as plt

x, y = [], []

with open("distances.txt", encoding="utf-8") as f:
    for line in f:
        if "–" in line:
            a, b = line.split("–", 1)
            x.append(float(a.strip()))
            y.append(float(b.strip()))

plt.plot(x, y)
plt.grid()
plt.show()