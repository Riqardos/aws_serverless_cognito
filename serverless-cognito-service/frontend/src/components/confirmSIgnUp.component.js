import React, { useState } from "react";
import { BASE_URL } from "../config";

export default function Login() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();

        fetch(`${BASE_URL}/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password }),
        })
            .then(response => response.json())
            .then(data => {
                console.log('Success:', data);
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    }
    return (
        <form>

            <h3>Log in</h3>

            <div className="form-group">
                <label>Username</label>
                <input type="text" value={username} onChange={e => { setUsername(e.target.value) }} className="form-control" placeholder="Enter username" />
            </div>

            <div className="form-group">
                <label>Password</label>
                <input type="password" value={password} onChange={e => { setPassword(e.target.value) }} className="form-control" placeholder="Enter password" />
            </div>

            <div className="form-group">
                <div className="custom-control custom-checkbox">
                    <input  type="checkbox" className="custom-control-input" id="customCheck1" />
                    <label className="custom-control-label" htmlFor="customCheck1">Remember me</label>
                </div>
            </div>

            <button type="submit" onClick={handleSubmit} className="btn btn-dark btn-lg btn-block">Sign in</button>
            {/* <p className="forgot-password text-right">
                Forgot <a href="#">password?</a>
            </p> */}
        </form>
    );
}

