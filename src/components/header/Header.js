import React, { Component } from 'react';
import { AppBar, List, ListItem, ListItemText, Toolbar, Typography, withTheme } from '@material-ui/core';
import { Link } from 'react-router-dom';

class Header extends Component {
    render() {
        return (
            <div className="header-nav">
                <AppBar position="static">
                    <Toolbar>
                        <Link className="header-item" to="/">
                            <Typography variant="h6">
                                Good Stoop
                            </Typography>
                        </Link>

                        <List component="nav">
                            <ListItem component="div">
                                <Link className="header-item" to="/building-complaints">
                                    <ListItemText inset>
                                        <Typography color="inherit" variant="title">
                                            Building Complaints
                                        </Typography>
                                    </ListItemText>
                                </Link>

                                <Link className="header-item" to="/nypd-complaints">
                                    <ListItemText inset>
                                        <Typography color="inherit" variant="title">
                                            NYPD Complaints
                                        </Typography>
                                    </ListItemText>
                                </Link>

                                <Link className="header-item" to="/restaurant-inspections">
                                    <ListItemText inset>
                                        <Typography color="inherit" variant="title">
                                            Restaurant Inspections
                                        </Typography>
                                    </ListItemText>
                                </Link>
                            </ListItem >
                        </List>
                    </Toolbar>
                </AppBar>
            </div>
        );
    }
}

export default Header;