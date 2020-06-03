import React, { useState, useEffect } from 'react';
import logo from './logo.svg';
import './App.css';
import axios from 'axios';

function App() {
  const [state,setState] = useState({
    currentTime: 0,
    boroughBoundaries: null
  })

  useEffect(() => {
    const getBoundaries = async () => {
      await axios.get('/api/borough-boundaries')
        .then(res => res.json())
        .then(data => {
          setState({...state, boroughBoundaries: data})
        });
    }
    fetch('/api/restaurant_inspection_results')
      .then(res => res.json())
      .then(data => {
        console.log(data);
    });
    
    getBoundaries();
  }, [state]);

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
        <p>NYC borough boundaries are {state.boroughBoundaries}</p>
      </header>
    </div>
  );
}

export default App;
