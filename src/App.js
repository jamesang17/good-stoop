import React, { useContext } from 'react';
import logo from './logo.svg';
import './App.css';
import { DataContext } from './components/providers/DataProvider';
import MapContainer from './components/map/MapContainer';


function App() {
  const { state } = useContext(DataContext);

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
      </header>
      {/* <MapContainer boroughBounds={state.nycBoundaries} nypdData={state.nypdComplaints}/> */}
    </div>
  );
}

export default App;
