import axios from 'axios';
import React, { useState } from "react";
import { Link, Redirect } from "react-router-dom";
import { BASE_URL } from "../config";

export default function SignUp() {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmSignUp, setConfirmSignUp] = useState(false);
    const [code, setCode] = useState('');
    const [redirect, setRedirect] = useState(false);
    const [loading, setLoading] = useState(false);
    const [loadingResend, setLoadingResend] = useState(false);


    const handleResendCode = (e) => {
        e.preventDefault();
        const conf = {
            url: `${BASE_URL}/resendCode`,
            method: "POST",
            data: JSON.stringify({ username }),
        };
        setLoadingResend(true);
        axios(conf)
            .then(res => {
                alert(res.data);
            })
            .catch(err => {
                console.log(err.response);
                alert(err.response.data)
            })
            .finally(() => {
                setLoadingResend(false);
            });
    }

    const handleSubmit = (e) => {
        e.preventDefault();

        const conf = {
            url: `${BASE_URL}/signUp`,
            method: "POST",
            data: JSON.stringify({ username, password, email }),
        };
        setLoading(true);
        axios(conf)
            .then(res => {
                setConfirmSignUp(true);
                alert(res.data);
            })
            .catch(err => {
                console.log(err.response);
                alert(err.response.data)
            })
            .finally(() => {
                setLoading(false);
            });
    }
    const handleConfirmCodeSubmit = (e) => {
        e.preventDefault();

        const conf = {
            url: `${BASE_URL}/confirmSignUp`,
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
            },
            data: JSON.stringify({ username, code }),
        };
        setLoading(true);

        axios(conf)
            .then(res => {
                setRedirect(true);
                console.log(res.response);
            })
            .catch(err => {
                console.log(err.response);

            })
            .finally(() => {
                setLoading(false);
            });
    }

    if (redirect) {
        return (<Redirect to='/sign-in' />)
    }

    return (
        <>
            <div className="outer">
                <div className="inner">
                    {
                        !confirmSignUp ?

                            <form>
                                <h3>Register</h3>

                                <div className="form-group">
                                    <label>Username</label>
                                    <input type="text" value={username} onChange={(e) => { setUsername(e.target.value) }} className="form-control" placeholder="Username" />
                                </div>

                                <div className="form-group">
                                    <label>Email</label>
                                    <input type="email" value={email} onChange={(e) => { setEmail(e.target.value) }} className="form-control" placeholder="Enter email" />
                                </div>

                                <div className="form-group">
                                    <label>Password</label>
                                    <input type="password" value={password} onChange={(e) => { setPassword(e.target.value) }} className="form-control" placeholder="Enter password" />
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
                                        <button type="submit" onClick={handleSubmit} className="btn btn-dark btn-lg btn-block">Register</button>

                                }

                                <p className="forgot-password text-right">
                                    Already registered
                <Link className="forgot-password" to={"/sign-in"}> log in?</Link>
                                </p>
                            </form>
                            :
                            <form>
                                <h3>Confirm registration</h3>

                                <div className="form-group">
                                    <label>Confirmation code</label>
                                    <div className="row">
                                        <div className="col-7">
                                            <input type="text" value={code} onChange={(e) => { setCode(e.target.value) }} className="form-control" placeholder="xxxxxxx" />

                                        </div>
                                        <div className="col-5">
                                            {
                                                loadingResend
                                                    ?
                                                    <div className="text-center" >
                                                        <div className="spinner-border " role="status">
                                                            <span className="sr-only">Loading...</span>
                                                        </div>
                                                    </div>
                                                    :
                                                    <div className="text-center" >
                                                        <button type="submit" onClick={handleResendCode} className="btn btn-outline-dark btn-block">Resend code</button>
                                                    </div>
                                            }
                                        </div>

                                    </div>

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
                                        <button type="submit" onClick={handleConfirmCodeSubmit} className="btn btn-dark btn-lg btn-block">Register</button>

                                }

                            </form>
                    }
                </div>
            </div>
        </>

    );
}