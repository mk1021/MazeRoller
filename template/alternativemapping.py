import matplotlib.pyplot as plt

# Define x and y values of the data points
x_values = [1, 2, 3, 4, 5]
y_values = [2, 4, 6, 8, 10]

# Plot the points and connect them with lines
plt.plot(x_values, y_values, '-o')

# Add labels and title
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Connected Dots')

# Display the graph
plt.show()
