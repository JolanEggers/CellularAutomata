# example of parametric probability density estimation
import statistics
import numpy as np

# generate a sample
from matplotlib import pyplot as plt

data=[]
names=["backToFront3Groups","frontToBack3Groups","randomSeating","steffenModified","windowMiddleAisle","steffenPerfect"]
colors=['blue','red','green','grey','purple','yellow']
# Read the data from the first CSV file
data.append(np.genfromtxt('results/backToFront3GroupsResult.csv', delimiter=','))

# Read the data from the second CSV file
data.append(np.genfromtxt('results/frontToBack3GroupsResult.csv', delimiter=','))

# Read the data from the third CSV file
data.append(np.genfromtxt('results/randomSeatingResult.csv', delimiter=','))

# Read the data from the 4. CSV file
data.append(np.genfromtxt('results/steffenModifiedResult.csv', delimiter=','))

# Read the data from the 4. CSV file
data.append(np.genfromtxt('results/windowMiddleAisleResult.csv', delimiter=','))

# Read the data from the 4. CSV file
data.append(np.genfromtxt('results/steffenPerfectResult.csv', delimiter=','))

std_dev=[]
mean=[]
for i in range(len(data)):
    std_dev.append(statistics.pstdev(data[i]))
    if std_dev[i]<10:
        std_dev[i]=20
    mean.append(statistics.mean(data[i]))
print(mean)
print(std_dev)

def plot_normal_distributions(means, std_devs, names, colors):
    x = np.linspace(np.min(means) - 3*np.max(std_devs), np.max(means) + 3*np.max(std_devs), 1000)

    for mean, std_dev, name, color in zip(means, std_devs, names, colors):
        y = (1/(std_dev * np.sqrt(2*np.pi))) * np.exp(-0.5*((x-mean)/std_dev)**2)
        plt.plot(x, y, label=f'{name} Mean={int(mean)}, Std Dev={int(std_dev)}',color=color)

    plt.title('Normal Distributions')
    plt.xlabel('X')
    plt.ylabel('Probability Density')
    plt.grid(True)
    plt.legend()
    plt.show()

plot_normal_distributions(mean,std_dev, names,colors)

'''
# Determine the common bin edges
min_value = min(np.min(data[0]), np.min(data[1]), np.min(data[2]), np.min(data[3]), np.min(data[4]), np.min(data[5]))
max_value = max(np.max(data[0]), np.max(data[1]), np.max(data[2]), np.max(data[3]), np.max(data[4]), np.max(data[5]))
num_bins = 30 # Adjust the number of bins as desired
bin_edges = np.linspace(min_value, max_value, num_bins + 1)

# Plot the PDF for data[0] in blue color
plt.hist(data[0], density=True, bins=bin_edges, color='blue', alpha=0.5, label=f"backToFront3Groups n={len(data[0])}")

# Plot the PDF for data[1] in red color
plt.hist(data[1], density=True, bins=bin_edges, color='red', alpha=0.5, label=f"frontToBack3Groups n={len(data[1])}")

# Plot the PDF for data[2] in green color
plt.hist(data[2], density=True, bins=bin_edges, color='green', alpha=0.5, label=f"randomSeating n={len(data[2])}")

# Plot the PDF for data[2] in green color
plt.hist(data[3], density=True, bins=bin_edges, color='grey', alpha=0.5, label=f"steffenModified n={len(data[3])}")

# Plot the PDF for data[2] in green color
plt.hist(data[4], density=True, bins=bin_edges, color='purple', alpha=0.5, label=f"windowMiddleAisle n={len(data[4])}")

# Plot the PDF for data[2] in green color
plt.hist(data[5], density=True, bins=bin_edges, color='yellow', alpha=0.5, label=f"steffenPerfect n={len(data[5])}")

#plt.yscale('log')
# Set the labels and title
plt.xlabel('Steps needed')
plt.ylabel('Probability Density')
plt.title('Probability Density Function')

# Display a legend
plt.legend()

# Display the plot
plt.show()
'''