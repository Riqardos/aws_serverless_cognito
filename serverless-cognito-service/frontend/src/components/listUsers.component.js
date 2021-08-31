import axios from "axios";
import React, { useEffect, useState } from "react";
import { BASE_URL } from "../config";

export default function ListUsers() {
    const [users, setUsers] = useState([]);
    const [loading, setLoading] = useState([]);

    const loadUsers = () => {
        setLoading(true);
        const IdToken = JSON.parse(localStorage.getItem("tokens"));
        if (IdToken) {
            const conf = {
                url: `${BASE_URL}/users`,
                method: "GET",
                timeout: 1000 * 2,
                headers: {
                    "Authorization": IdToken.IdToken
                }
            };

            axios(conf)
                .then(res => {
                    setUsers(res.data);
                })
                .catch(({response}) => {
                    alert(response.data.error)
                })
                .finally(()=>{
                    setLoading(false);
                })
        }
        else{
            alert("You must sign-in!");
        }

    }

    useEffect(() => {
        loadUsers();
    }, [])

    return (
        <>
            {
                loading
                    ?
                    <div className="text-center" >
                        <div className="spinner-border " role="status">
                            <span className="sr-only">Loading...</span>
                        </div>
                    </div>
                    :
                    <div className="container">

                        <table className="table table-light table-striped ">

                            <thead>
                                <tr>
                                    <th scope="col">#</th>
                                    <th scope="col">Username</th>
                                    <th scope="col">Email</th>
                                    <th scope="col">UserStatus</th>
                                    <th scope="col">Enabled</th>
                                    <th scope="col">UserCreateDate</th>


                                </tr>
                            </thead>
                            <tbody>
                                {
                                    users.map((item, index) => {
                                        return (
                                            <tr key={index}>
                                                <th scope="row">{index}</th>
                                                <td>{item.Username}</td>
                                                <td>{item.Attributes[2].Value}</td>
                                                <td>{item.UserStatus}</td>
                                                <td>{(item.Enabled ? "Enabled" : "Disabled")}</td>
                                                <td>{item.UserCreateDate}</td>
                                            </tr>

                                        )
                                    })
                                }
                            </tbody>
                        </table>
                    </div>
            }


        </>
    );
}

