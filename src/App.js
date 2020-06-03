import React, { useState, useEffect } from 'react';
import logo from './logo.svg';
import './App.css';
import axios from 'axios';

function App() {
  const [state, setState] = useState({
    currentTime: 0,
    boroughBoundaries: null
  })

  const getBoundaries = async () => {
    await axios.get('/api/borough_boundaries')
      .then(res => {
        console.log(res.data);
      });
  }

  const getBuildingComplaints = async () => {
    await axios.get('/api/building_complaint_results')
      .then(res => console.log(res))
  }

  const getNypdComplaints = async () => {
    await axios.get('/api/nypd_complaint_results')
      .then(res => console.log(res))
  }

  const getRestaurantInspectionResults = async () => {
    await axios.get('/api/restaurant_inspection_results')
      .then(res => {
        console.log(res.data);
      });
  }

  useEffect(() => {
    getBoundaries();
    getBuildingComplaints();
    getNypdComplaints();
    getRestaurantInspectionResults();
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
        <p>The current time is {state.currentTime}.</p>
        <p>NYC borough boundaries are {String(state.boroughBoundaries)}</p>
      </header>
    </div>
  );
}

export default App;
