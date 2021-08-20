import axios from 'axios';
import React, { useState } from "react";
import { Redirect } from 'react-router';
import { BASE_URL } from "../config";

export default function ForgotPassword() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [code, setCode] = useState('');
    const [loading, setLoading] = useState(false);
    const [confirm, setConfirm] = useState(false);
    const [redirect, setRedirect] = useState(false);

    const handleReset = (e) => {
        e.preventDefault();

        const conf = {
            url: `${BASE_URL}/forgotPassword`,
            method: "POST",
            data: JSON.stringify({ username})
        };

        setLoading(true);

        axios(conf)
            .then(res => {
                setConfirm(true);
                alert(`Confirmation code sent to ${res.data.Destination}`);
            })
            .catch(err => {
                alert(err.response.data)
            })
            .finally(() => {
                setLoading(false);
            })

    }


    const handleConfirm = (e) => {
        e.preventDefault();

        const conf = {
            url: `${BASE_URL}/confirmForgottenPassword`,
            method: "POST",
            data: JSON.stringify({ username, password, code })
        };

        setLoading(true);

        axios(conf)
            .then(res => {
                alert("Reset OK!");
                setRedirect(true);
            })
            .catch(err => {
                alert(err.response.data)
            })
            .finally(() => {
                setLoading(false);
            })
    }

    if (redirect){
        return <Redirect to='/sign-in'/>; 
    }

    return (
        <div className="outer">
            <div className="inner">
                {
                    !confirm ?
                        <form>

                            <h3>Forgot password?</h3>

                            <p>Confirmation code will be send to your email.</p>
                            <div className="form-group">
                                <label>Username</label>
                                <input type="text" value={username} onChange={e => { setUsername(e.target.value) }} className="form-control" placeholder="Enter username" />
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
                                    <button type="submit" onClick={handleReset} className="btn btn-dark btn-lg btn-block">Reset password</button>

                            }
                        </form>
                        :
                        <form>
                            <h3>Reset password</h3>
                            <div className="form-group">
                                <label>Code</label>
                                <input type="text" value={code} onChange={e => { setCode(e.target.value) }} className="form-control" placeholder="Enter username" />
                            </div>

                            <div className="form-group">
                                <label>New password</label>
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
                                    <button type="submit" onClick={handleConfirm} className="btn btn-dark btn-lg btn-block">Reset password</button>

                            }
                        </form>

                }

            </div>
        </div>

    );
}

