import csv
import matplotlib.pyplot as plt

# Read data from the first CSV file
x1 = []
y1 = []
with open('results/windowMiddleAisleLuggage.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        x1.append(float(row[0]))
        y1.append(float(row[1]))

# Read data from the second CSV file
x2 = []
y2 = []
with open('results/backToFront3GroupsLuggage.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        x2.append(float(row[0]))
        y2.append(float(row[1]))

# Create the XY plot with lines and marked points for both datasets
plt.plot(x1, y1, '-o', label='windowMiddleAisle', marker='x', markersize=8, linewidth=1)
plt.plot(x2, y2, '-o', label='backToFront3Groups', marker='x', markersize=8, linewidth=1)
plt.xlabel('luggage storing time')
plt.ylabel('steps needed')
plt.title('')
plt.legend()
plt.show()
