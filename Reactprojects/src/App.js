import React, { useEffect, useState } from 'react';
import './App.css';
import AWS from 'aws-sdk';

AWS.config.update({
  accessKeyId: 'YOUR_ACCESS_KEY_ID',
  secretAccessKey: 'YOUR_SECRET_ACCESS_KEY',
  region: 'YOUR_REGION',
});

function App() {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isMoving, setIsMoving] = useState(false);
  const [lines, setLines] = useState([
      /*{ x: 100, y: 100 },
      { x: 200, y: 100 },
      { x: 200, y: 200 },
      { x: 300, y: 200 },
    */
  ]);
  const [intervalId, setIntervalId] = useState(null);
  const [pathLines, setPathLines] = useState([]);
  const [bestRoute, setBestRoute] = useState([]);
  //const containerHeight = 421;
  //const [, updatecoordinateArray] = useState([[]]);

  /*const updateCoordinateArray = (nextCoordinate) => {
    setLines((prevLines) => [...prevLines, nextCoordinate]);
  };*/

  React.useEffect(() => {
    const fetchCoordinates = () => {
      fetch("http://localhost:3001/nextCoordinate")
        .then((res) => res.json())
        .then((data) => {
          //const coordinate = {x: data.x, y: data.y};
          //setLines((prevLines) => [...prevLines, data]);
          setLines(data);
          setCurrentIndex((prevIndex) => prevIndex + 1);
          //updateCoordinateArray(data);
          console.log('fetch successful:', data);
          console.log('lines array:', lines)
        })
        .catch((err) =>console.error('Error fetching coordinates:', err)); //alert(err));
    }; 

    //handleClick is our event handler for the button click
    /*const handleClick = (updateMethod) => {
    fetch("http://localhost:3001/nextCoordinate/")
    .then((res) => res.json())
    .then((data) => updateMethod(data.nextCoordinate))
    .catch((err) => alert(err)
    );
    };*/

  //useEffect(() => {
    if (isMoving) {
      const id = setInterval(() => {
        fetchCoordinates();
        //setCurrentIndex((prevIndex) =>   prevIndex + 1);
        console.log('in the fetching loop');
          /*const nextIndex = prevIndex + 1;
          if (nextIndex >= lines.length) {
            setIsMoving(false);
            clearInterval(intervalId);
            return prevIndex; // Add this line to prevent going out of bounds
          }
          setPathLines((prevPathLines) => [...prevPathLines, lines[nextIndex]]);
          return nextIndex;
        });*/
      }, 1000);
      setIntervalId(id);
    } else {
      clearInterval(intervalId);
    }

    return () => {
      clearInterval(intervalId);
    };
  }, [isMoving/*, intervalId, lines, currentIndex/*, coordinateArray*/]);

  const handleStart = () => {
    setIsMoving(true);
    setPathLines([...lines.slice(0, currentIndex + 1)]);
    //setLines([]);
    console.log('Started');
    setCurrentIndex(0);
  };

  const handleFindBestRoute = () => {
    /*fetch("http://localhost:3001/bestRoute")
      .then((res) => res.json())
      .then((data) => {
        setBestRoute(data);
        console.log("Best route:", data);
      })
      .catch((err) => console.error('Error finding best route:', err));// alert(err));*/
      console.log('Finding the best route...');
    };

  return (
    <div className="container">
      <h1>The Maze Roller's Map</h1>
      <div className="rectangle">
        {pathLines.map((coordinate, index) => {
          if (index < pathLines.length - 1) {
            const nextCoordinate = pathLines[index + 1];
            console.log('Taken in the next coordinate');
            return (
              <div
                key={index}
                className="line"
                style={{
                  top: `${421 - coordinate.y}px`,
                  left: `${coordinate.x}px`,
                  width: `${Math.sqrt(
                    Math.pow(nextCoordinate.x - coordinate.x, 2) +
                    Math.pow(nextCoordinate.y - coordinate.y, 2)
                  )}px`,
                  transform: `rotate(${Math.atan2(
                    nextCoordinate.y - coordinate.y,
                    nextCoordinate.x - coordinate.x
                  )}rad)`,
                  
              //display: index === 0 ? 'none' : 'block', //only draws lines between first plotted point onwards
                }}
              ></div>
            );
          }
          console.log('Draw line return finished');
          return null;
        })}
        {bestRoute.map((coordinate, index) => (
          <div
            key={index}
            className="best-route-line"
            style={{ 
              top: `${421 - coordinate.y}px`, 
              left: `${coordinate.x}px`,
            }}
          ></div>
        ))}
        <div 
          className="square"
          style={{
            top: `${421 - lines[currentIndex]?.y}px`,
            left: `${lines[currentIndex]?.x}px`,
          }}
        ></div>
      </div>
      <button onClick={handleStart} disabled={isMoving}>
        Start
      </button>
      <button onClick={handleFindBestRoute} disabled={isMoving}>
        Find Best Route
      </button>
    </div>
  );
}

export default App;
