import React, { Component } from 'react';
import { Navbar, Nav } from 'react-bootstrap';

class Header extends Component {
    render() {
        return (
            <div className="header-nav">
                <Navbar bg="light" expand="lg" fixed="top">
                    <Navbar.Brand href="/">Good-Stoop</Navbar.Brand>
                    <Navbar.Toggle aria-controls="basic-navbar-nav" />
                    <Navbar.Collapse id="basic-navbar-nav">
                        <Nav className="mr-auto">
                            <Nav.Link href="/building-complaints">Building Complaints</Nav.Link>
                            <Nav.Link href="/nypd-complaints">NYPD Complaints</Nav.Link>
                            <Nav.Link href="/restaurant-inspections">Restaurant Inspections</Nav.Link>
                        </Nav>
                    </Navbar.Collapse>
                </Navbar>
            </div>
        );
    }
}

export default Header;