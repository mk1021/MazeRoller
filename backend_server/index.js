const express = require("express");
const cors = require('cors');

const PORT = process.env.PORT || 3001;
const app = express();

app.use(cors({
 origin: '*'
}));
app.use(cors({
 methods: ['GET','POST','DELETE','UPDATE','PUT','PATCH']
}));
app.use(express.json());

let currentIndex = 0;

const coordinateArray = [
    { x: 0, y: 0 },
    { x: 100, y: 100 },
    { x: 200, y: 100 },
    { x: 300, y: 200 },
    { x: 300, y: 100 },
    // Add more coordinate objects as needed
];

app.get("/nextCoordinate", (req, res) => {
    if (currentIndex >= coordinateArray.length) {
      currentIndex = 0; // Reset the index if all coordinates have been sent
    }
  
    const nextCoordinate = coordinateArray[currentIndex];
    currentIndex++;
  
    res.json(nextCoordinate);
});

/* endpoints for esp, ec2, database, best route*/

// data is being sent to the server with a post request
app.post('/esp32/', (req, res) => {
    const { x, y } = req.body;
    console.log('Received coordinates:', x, y);
    //const repsonseContent = "<p>Received data: " + postData.i + postData.j + "</p>";
    
    //store rover coordinates in a local array 
    var roverxyall = [];
    //const roverxy = postData.split(",");
    roverxyall.push([(x),(y)]);  // requires scaling
    console.log('current rover position: ' + x, y);
    res.sendStatus(202); //reponse when data has been received (ok)
});

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
  
app.listen(PORT, () => {
    console.log(`Server listening on ${PORT}`);
});
