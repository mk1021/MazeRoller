import matplotlib.pyplot as plt
import boto3

# # Connect to DynamoDB
# dynamodb = boto3.resource('dynamodb')
# table = dynamodb.Table('your_table_name')  # Replace 'your_table_name' with your actual table name

# # Fetch data from DynamoDB
# response = table.scan()
# items = response['Items']

items = [(2, 4), (5, 7), (1, 8), (6, 8)]

# Extract x and y coordinates from the fetched items
x_values = [item['x'] for item in items]
y_values = [item['y'] for item in items]

# Plot the coordinates
plt.scatter(x_values, y_values)
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Coordinate Graph')

# Display the plot
plt.show()
