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
            url: `${BASE_URL}/login/password/reset`,
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
            url: `${BASE_URL}/login/password/reset/confirm`,
            method: "POST",
            data: JSON.stringify({ username, password, code })
        };

        setLoading(true);

        axios(conf)
            .then(({data}) => {
                alert(data.message);
                setRedirect(true);
            })
            .catch(({response}) => {
                alert(response.data.error)
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
                                    <div className="text-center" >
                                        <div className="spinner-border " role="status">
                                            <span className="sr-only">Loading...</span>
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
                                    <div className="text-center" >
                                        <div className="spinner-border " role="status">
                                            <span className="sr-only">Loading...</span>
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

