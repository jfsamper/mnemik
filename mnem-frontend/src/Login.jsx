import React, { useState, useEffect } from 'react';
import { Session } from 'react-session';

function Login() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [authenticated, setAuthenticated] = useState(false);
    

    useEffect(() => {
        if (authenticated) {
            window.location.href = '/items';
        }    
    }, []);

const handleSubmit = async (event) => {
    event.preventDefault();
    try {
        const response = await fetch('http://localhost:5000/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: username,
                password: password
            })
        });
        const data = await response.json();
        if (data.success) {
            //set session to ('user_id', data.user_id)
            alert('Login successful!');            
            setAuthenticated(true);
            setError('');
            // Redirect to items page while logged in
            window.location.href = '/items';
        } else {
            // Display an error message based on the response
            if (data.message === 'Invalid credentials') {
                // Display an error message for wrong username or password
                setError('Invalid username or password');
            } else {
                // Display a generic error message
                setError('An error occurred. Please try again.');
            }
        }
    } catch (error) {
        console.error(error);
        // Display a generic error message
        setError('An error occurred. Please try again.');
    }
};

    return (
        <div>
            <h2>Login</h2>
            <form onSubmit={handleSubmit}>
                <label>
                    Username:
                    <input
                        type="text"
                        value={username}
                        onChange={(event) => setUsername(event.target.value)}
                    />
                </label>
                <br/>
                <label>
                    Password:
                    <input
                        type="password"
                        value={password}
                        onChange={(event) => setPassword(event.target.value)}
                    />
                </label>
                <br/>
                <button type="submit">Login</button>
                {error && <p className="error">{error}</p>}
            </form>
        </div>
    );
}

export default Login;