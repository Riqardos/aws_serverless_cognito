import axios from 'axios';
import React, { useState } from "react";
import { BASE_URL } from "../config";

export default function Login() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSubmit = (e) => {
        e.preventDefault();

        const conf = {
            url: `${BASE_URL}/login`,
            method: "POST",
            data: JSON.stringify({ username, password })
        };

        setLoading(true);

        axios(conf)
            .then(res => {
                alert("Logged in!");
                localStorage.setItem('tokens', JSON.stringify(res.data))
            })
            .catch(err => {
                alert(err.response.data)
            })
            .finally(() => {
                setLoading(false);
            })

    }
    return (
        <div className="outer">
            <div className="inner">
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

                    {
                        loading
                            ?
                            <div class="text-center" >
                                <div class="spinner-border " role="status">
                                    <span class="sr-only">Loading...</span>
                                </div>
                            </div>
                            :
                            <button type="submit" onClick={handleSubmit} className="btn btn-dark btn-lg btn-block">Sign in</button>

                    }
                    <p className="forgot-password text-right">
                        Forgot <a href="/forgot">password?</a>
                    </p>
                </form>
            </div>
        </div>

    );
}

