import React, { useState, useEffect } from 'react';
import axios from 'axios';

export const DataContext = React.createContext();

export const DataProvider = ({ children }) => {
  const [state, setState] = useState({
    currentTime: 0,
    nycBoundaries: null,
    nypdComplaints: null,
    buildComplaints: null,
    restData: null
  })

  const getBoundaries = async () => {
    if (localStorage.hasOwnProperty("nycBoundaries")) {
      console.log("Using cached boundary data.");
      let value = localStorage.getItem("nycBoundaries");
      try {
        value = JSON.parse(value);
        console.log(value);
        setState({ ...state, nycBoundaries: value });
      } catch (e) {
        console.error(e);
      }
    } else {
      await axios.get('/api/borough_boundaries')
        .then(res => {
          console.log(res.data);
          localStorage.setItem("nycBoundaries", JSON.stringify(res.data))
        });
    }
  }

  const getBuildingComplaints = async () => {
    await axios.get('/api/building_complaint_results')
      .then(res => { 
        console.log(res.data);
        setState({ ...state, buildComplaints: res.data });
      });
  }

  const getNypdComplaints = async () => {
    await axios.get('/api/nypd_complaint_results')
      .then(res => { 
        console.log(res.data);
        setState({ ...state, nypdComplaints: res.data });

      });
  }

  const getRestaurantInspectionResults = async () => {
    await axios.get('/api/restaurant_inspection_results')
      .then(res => { 
        console.log(res.data);
        setState({ ...state, restData: res.data });
      });
  }

  useEffect(() => {
    getBoundaries();
    getBuildingComplaints();
    getNypdComplaints();
    getRestaurantInspectionResults();
  }, []);

  return (
    <DataContext.Provider
      value={{
        state
      }}
    >
      {children}
    </DataContext.Provider>
  )
}