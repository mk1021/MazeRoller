const express = require("express");
const cors = require('cors');
const AWS = require('aws-sdk');
//const path = require('path');

const PORT = process.env.PORT || 3001;
const app = express();

//app.use(cors());
app.use(cors({
 origin: '*'
}));

//app.use(express.static(path.resolve(__dirname, './my-app/build')));

app.use(cors({
 methods: ['GET','POST','DELETE','UPDATE','PUT','PATCH']
}));

app.use(express.json());


let currentIndex = 0;
let coordinateArray = [];

//array for testing fetching
/*const coordinateArray = [
    { x: 0, y: 0 },
    { x: 100, y: 100 },
    { x: 200, y: 100 },
    { x: 300, y: 200 },
    { x: 300, y: 100 },
    // Add more coordinate objects as needed
];*/

// Configure the AWS credentials and region
AWS.config.update({
  accessKeyId: 'YOUR_AWS_ACCESS_KEY',
  secretAccessKey: 'YOUR_AWS_SECRET_ACCESS_KEY',
  region: 'us-east-1' // Change to your desired region
});

// Create a DynamoDB DocumentClient
const dynamodb = new AWS.DynamoDB.DocumentClient();

// Function to fetch and record the current coordinates
function fetchCurrentCoordinates() {
  const params = {
    TableName: 'Coordinates',
    //Key: { id: 1 }
    KeyConditionExpression: '#id = :id',  //condition for query 
    ExpressionAttributeNames: {
      '#id': 'id',
    },
    ExpressionAttributeValues: {
      ':id': 'coordinates',
    },
    ScanIndexForward: true,  //ensures results are returned in ascending order  
  };

  /*dynamodb.get(params, function(err, data) {  //DO NOT NEED THIS
    if (err) {
      console.error("Error:", err);
    } else {
      const coordinates = data.Item.coordinates;
      console.log("Current coordinates:", coordinates);
      // Perform further processing or store the coordinates in a variable
    }
  });
}*/

  dynamodb.query(params, (err, data) => {
    if (err) {
      console.error('Error fetching coordinates from DynamoDB:', err);
      return;
    }

    if (data.Items && data.Items.length > 0) {
      coordinateArray = data.Items[0].coordinates.map(([x, y]) => ({ x, y }));
      console.log('Coordinates fetched from DynamoDB:', coordinateArray);
    }
  });
}

// Call the fetchCurrentCoordinates function at a regular interval
setInterval(fetchCurrentCoordinates, 1000); // Check every 1 seconds

app.get("/nextCoordinate", (req, res) => {
    if (currentIndex >= coordinateArray.length) {
      currentIndex = 0;
      return res.sendStatus(204); // Send a "No Content" response to indicate the end of the array
    }
  
    const nextCoordinate = coordinateArray[currentIndex];
    currentIndex++;
  
    res.json(nextCoordinate);
});

/* endpoints for esp, ec2, database, best route*/

// data is being sent to the server with a post request
/*app.post('/esp32/', (req, res) => {
    const { x, y } = req.body;
    console.log('Received coordinates:', x, y);
    //const repsonseContent = "<p>Received data: " + postData.i + postData.j + "</p>";
    
    //store rover coordinates in a local array 
    var roverxyall = [];
    //const roverxy = postData.split(",");
    roverxyall.push([(x),(y)]);  // requires scaling
    console.log('current rover position: ' + x, y);
    res.sendStatus(202); //reponse when data has been received (ok)
});*/

app.get("/bestRoute", (req, res) => {
    if (coordinateArray.length === 0) {
      res.status(400).json({ message: "No coordinates available" });
      return;
    }
  
    // Run the algorithm to find the best route
    const bestRoute = findBestRoute(coordinateArray);
  
    res.json(bestRoute);
});
  
  function findBestRoute(coordinates) {
    // Implement algorithm to find the best route here
    // can be Dijkstra's algorithm, A* algorithm, or any other suitable algorithm
  
    // Return an array of coordinates representing the best route through the maze
    // Example: [{ x: 0, y: 0 }, { x: 100, y: 100 }, { x: 200, y: 100 }, ...]
  }

/*function random() {
    const min = 20;
    const max1 = 570; 
    const max2 = 320;

    var arr = [];
    arr = [Math.floor(Math.random() * (max1 - min + 1)) + min, Math.floor(Math.random() * (max2 - min + 1)) + min];
    console.log("random coordinates:", arr);
    return arr;
}*/
  
/*app.get('*', (req, res) => {
  res.sendFile(path.resolve(__dirname, './my-app/build', 'index.html'));
});*/

app.listen(PORT, () => {
    console.log(`Server listening on ${PORT}`);
});
