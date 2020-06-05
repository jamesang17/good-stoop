import React, { Component } from 'react';
import Header from './header/Header';

class Home extends Component {
    render() {
        return (
            <div className="home-page">
                <Header />
                Home Page
            </div>
        );
    }
}

export default Home;