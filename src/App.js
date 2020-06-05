import React from 'react';
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import './App.css';
import Header from './components/header/Header';
import Home from './components/Home';
import BuildingComplaints from './components/BuildingComplaints';
import NypdComplaints from './components/NypdComplaints';
import RestaurantInspections from './components/RestaurantInspections';


function App() {
  return (
    <Router>
      <Header />

      <Switch>
        <Route path="/building-complaints">
          <BuildingComplaints />
        </Route>

        <Route path="/nypd-complaints">
          <NypdComplaints />
        </Route>

        <Route path="/restaurant-inspections">
          <RestaurantInspections />
        </Route>

        <Route path="/">
          <Home />
        </Route>
      </Switch>
    </Router>
  );
}

export default App;
