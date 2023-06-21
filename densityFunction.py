# example of parametric probability density estimation
import numpy as np

# generate a sample
from matplotlib import pyplot as plt

# Read the data from the first CSV file
data1 = np.genfromtxt('results/backToFront3GroupsResult.csv', delimiter=',')

# Read the data from the second CSV file
data2 = np.genfromtxt('results/frontToBack3GroupsResult.csv', delimiter=',')

# Read the data from the third CSV file
data3 = np.genfromtxt('results/randomSeatingResult.csv', delimiter=',')

# Read the data from the 4. CSV file
data4 = np.genfromtxt('results/steffenModifiedResult.csv', delimiter=',')

# Read the data from the 4. CSV file
data5 = np.genfromtxt('results/windowMiddleAisleResult.csv', delimiter=',')

# Read the data from the 4. CSV file
data6 = np.genfromtxt('results/steffenPerfectResult.csv', delimiter=',')

# Determine the common bin edges
min_value = min(np.min(data1), np.min(data2), np.min(data3), np.min(data4), np.min(data5), np.min(data6))
max_value = max(np.max(data1), np.max(data2), np.max(data3), np.max(data4), np.max(data5), np.max(data6))
num_bins = 30 # Adjust the number of bins as desired
bin_edges = np.linspace(min_value, max_value, num_bins + 1)

# Plot the PDF for data1 in blue color
plt.hist(data1, density=True, bins=bin_edges, color='blue', alpha=0.5, label=f"backToFront3Groups n={len(data1)}")

# Plot the PDF for data2 in red color
plt.hist(data2, density=True, bins=bin_edges, color='red', alpha=0.5, label=f"frontToBack3Groups n={len(data2)}")

# Plot the PDF for data3 in green color
plt.hist(data3, density=True, bins=bin_edges, color='green', alpha=0.5, label=f"randomSeating n={len(data3)}")

# Plot the PDF for data3 in green color
plt.hist(data4, density=True, bins=bin_edges, color='grey', alpha=0.5, label=f"steffenModified n={len(data4)}")

# Plot the PDF for data3 in green color
plt.hist(data5, density=True, bins=bin_edges, color='purple', alpha=0.5, label=f"windowMiddleAisle n={len(data5)}")

# Plot the PDF for data3 in green color
plt.hist(data6, density=True, bins=bin_edges, color='yellow', alpha=0.5, label=f"steffenPerfect n={len(data6)}")

#plt.yscale('log')
# Set the labels and title
plt.xlabel('Steps needed')
plt.ylabel('Probability Density')
plt.title('Probability Density Function')

# Display a legend
plt.legend()

# Display the plot
plt.show()