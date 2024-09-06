import React, { useState, useEffect } from 'react';
import { login, isAuthenticated } from './services/auth';

function Login() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');

const handleSubmit = async (event) => {
    event.preventDefault();
    try { 
        const response = await login(username, password);
        if (response.success) { // Check if the response indicates success
            alert('Login successful!');            
            setError('');
            localStorage.setItem('username', username);
        } else {
                // Display a generic error message
                setError('An error occurred. Please try again.');
        }
        
    } catch (error) {
        console.error(error);
        if (error.response && error.response.status === 401) {
            // Display an authentication error message
            setError('Invalid username or password. Please try again.');
        } else {
            setError('A network error occurred. Please try again.');   
        }
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
                {!error && isAuthenticated() && (
                    <div>
                    <h2>Authenticated!</h2>
                    <button onClick={() => setUsername('')}>Logout</button>
                    <p>Welcome {username}</p>
                    </div>
                )}
            </form>
        </div>
    );
}

export default Login;