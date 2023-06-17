import React, { useEffect, useState } from 'react';
import './App.css';

function App() {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isMoving, setIsMoving] = useState(false);
  const [lines, setLines] = useState([]);
  const [intervalId, setIntervalId] = useState(null);
  const [bestRoute, setBestRoute] = useState([]);

  //const [, updatecoordinateArray] = useState([[]]);

  const updateCoordinateArray = (nextCoordinate) => {
    setLines((prevLines) => [...prevLines, nextCoordinate]);
  }; 
  
  useEffect(() => {
    const fetchCoordinates = () => {
      fetch("http://localhost:3001/nextCoordinate")
        .then((res) => res.json())
        .then((data) => {
          //setLines((prevLines) => [...prevLines, data]);
          updateCoordinateArray(data);
          console.log("fetch successful");
        })
        .catch((err) => alert(err));
    };

  /*const fetchCoordinates = () => {
    const coordinate = lines[currentIndex];
    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(coordinate),
    };

    fetch('http://localhost:3001/esp32/', requestOptions)
      .then(() => {
        console.log('Coordinates sent:', coordinate);
        setCurrentIndex((prevIndex) => prevIndex + 1);
      })
      .catch((err) => alert(err));
  };*/

  //handleClick is our event handler for the button click
    /*const handleClick = (updateMethod) => {
    fetch("http://localhost:3001/nextCoordinate/")
    .then((res) => res.json())
    .then((data) => updateMethod(data.nextCoordinate))
    .catch((err) => alert(err)
    );
    };*/

    const moveSquare = () => {
      const square = document.querySelector('.square');
      const rectangle = document.querySelector('.rectangle');

      const squareRect = square.getBoundingClientRect();
      const rectangleRect = rectangle.getBoundingClientRect();

      const maxTop = rectangleRect.height - squareRect.height;
      const maxLeft = rectangleRect.width - squareRect.width;

      const coordinateArray = lines;

      if (currentIndex >= coordinateArray.length) {
        clearInterval(intervalId);
        return;
      }
      
      const coordinate = coordinateArray[currentIndex];
      const randomTop = maxTop - coordinate.y;
      const randomLeft = coordinate.x;

      square.style.top = `${randomTop}px`;
      square.style.left = `${randomLeft}px`;

      const line = { x: randomLeft, y: randomTop };
      setLines((prevLines) => [...prevLines, line]);

      /*if (currentIndex === coordinateArray.length - 1) {
        clearInterval(intervalId);
      } else {*/
        setCurrentIndex((prevIndex) => prevIndex + 1);
    };

    //useEffect(() => {
      if (isMoving) {
        const id = setInterval(fetchCoordinates, 1000);
        setIntervalId(id);
      } else {
        clearInterval(intervalId);
      }

      return () => {
        clearInterval(intervalId);
      };
  }, [isMoving, currentIndex/*, coordinateArray*/]);

  const handleStart = () => {
    setIsMoving(true);
    setLines([]);
    setCurrentIndex(0);
  };

  const handleFindBestRoute = () => {
    fetch("http://localhost:3001/bestRoute")
      .then((res) => res.json())
      .then((data) => {
        setBestRoute(data);
        console.log("Best route:", data);
      })
      .catch((err) => alert(err));
  };
  
  return (
    <div className="container">
      <h1>The Maze Roller's Map</h1>
      <div className="rectangle">
        {lines.map((line, index) => (
          <div
            key={index}
            className="line"
            style={{ top: line.y, left: line.x }}
          ></div>
        ))}
        {bestRoute.map((coordinate, index) => (
          <div
            key={index}
            className="best-route-line"
            style={{ top: coordinate.y, left: coordinate.x }}
          ></div>
        ))}
        <div className="square"></div>
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
