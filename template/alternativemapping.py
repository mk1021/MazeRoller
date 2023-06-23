import matplotlib.pyplot as plt
import time
import boto3#


# # Define x and y values of the data points
# x_values = [1, 2, 3, 4, 5]
# y_values = [2, 4, 6, 8, 10]
#
# # Plot the points and connect them with lines
# plt.plot(x_values, y_values, '-o')
#
# # Add labels and title
# plt.xlabel('X')
# plt.ylabel('Y')
# plt.title('Connected Dots')
#
# # Display the graph
# plt.show()

# -------------------------------------- A C T U A L    C O D E ----------------------------------------
import matplotlib.pyplot as plt
import time
import boto3

# Initialize the DynamoDB client
dynamodb = boto3.client('dynamodb')

# Define empty lists to store x and y values
x_values = []
y_values = []

# Function to fetch data from DynamoDB
def fetch_data_from_dynamodb():
    response = dynamodb.scan(
        TableName='your_table_name'
    )
    items = response['Items']
    for item in items:
        x_tuple = item['coordinates']['L'][0]['N']  # x-coordinate is at index 0 of the tuple
        y_tuple = item['coordinates']['L'][1]['N']  # y-coordinate is at index 1 of the tuple
        x_values.append(float(x_tuple))
        y_values.append(float(y_tuple))

# Function to update the plot
def update_plot():
    plt.clf()  # Clear the current plot
    plt.plot(x_values, y_values, '-o')  # Plot the points and connect them with lines
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Connected Dots')
    plt.draw()  # Redraw the plot

# Main loop
while True:
    fetch_data_from_dynamodb()  # Fetch data from DynamoDB
    update_plot()  # Update the plot
    time.sleep(1)  # Sleep for 1 second before fetching data again
