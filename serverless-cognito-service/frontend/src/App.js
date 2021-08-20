import axios from 'axios';
import React, { useState } from 'react';
import { BrowserRouter as Router, Link, Route, Switch } from "react-router-dom";
import '../node_modules/bootstrap/dist/css/bootstrap.min.css';
import './App.css';
import ForgotPassword from './components/forgotPassword.component';
import ListUsers from './components/listUsers.component';
import Login from "./components/login.component";
import SignUp from "./components/signup.component";
import { BASE_URL } from './config';


function App() {

  const handleRefreshToken = () => {

    const token = JSON.parse(localStorage.getItem("tokens"));
    if (token) {
      const conf = {
        url: `${BASE_URL}/refreshToken`,
        method: "POST",
        data: JSON.stringify({ refresh_token: token['RefreshToken'] })
      };


      axios(conf)
        .then(res => {
          alert("Tokens refreshed!");
          localStorage.setItem("tokens", JSON.stringify({ ...token, ...res.data }))
        })
        .catch(err => {
          alert(err.response.data)
        })
        .finally(() => {
        })
    }
    else{
      alert("No valid token!")
    }

  }

  return (<Router>
    <div className="App">
      <nav className="navbar navbar-expand-lg navbar-light ">
        <div className="container">
          <Link className="navbar-brand" to={"/sign-in"}>Cognito demo app</Link>
          <div className="collapse navbar-collapse" id="navbarTogglerDemo02">
            <ul className="navbar-nav ml-auto">
              <li className="nav-item">
                <Link className="nav-link" to={"/sign-in"}>Login</Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link" to={"/sign-up"}>Sign up</Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link" to={"/list-users"}>List users</Link>
              </li>
              <li className="nav-item">
                <Link
                  className="nav-link"
                  onClick={() => {
                    handleRefreshToken()
                  }}>
                  Refresh token
                    </Link>
              </li>
              <li className="nav-item">
                <Link
                  className="nav-link"
                  onClick={() => {
                    localStorage.removeItem('tokens')
                  }} to={"/sign-in"}>

                  Logout
                    </Link>
              </li>

            </ul>
          </div>
        </div>
      </nav>
      <div className="container mt-5">
        <Switch>

          <Route exact path='/' component={Login} />
          <Route path="/sign-in" component={Login} />
          <Route path="/sign-up" component={SignUp} />
          <Route path="/forgot" component={ForgotPassword} />
          <Route path="/list-users" component={ListUsers} />

        </Switch>

      </div>


    </div></Router>
  );
}

export default App;
