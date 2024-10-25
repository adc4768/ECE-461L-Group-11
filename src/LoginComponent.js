import React, { useState } from 'react';

const LoginComponent = () => {
    const [loginCredentials, setLoginCredentials] = useState({ username: '', password: '' });

    const handleLoginChange = (e) => {
        const { name, value } = e.target;
        setLoginCredentials(prev => ({ ...prev, [name]: value }));
    };

    const handleLoginSubmit = (e) => {
        e.preventDefault();
        console.log('Login Attempted:', loginCredentials);
        // Add your login logic here
    };

    const handleCreateAccountClick = () => {
        console.log('Create Account button clicked');
        // Add your create account logic or navigation here
    };

    return (
        <div style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            minHeight: '100vh',
            textAlign: 'center',
            padding: '20px',
        }}>
            <h1 style={{ fontSize: '2rem', fontWeight: 'bold', marginBottom: '20px' }}>Login</h1>

            <div style={{
                border: '1px solid #ddd',
                borderRadius: '8px',
                padding: '20px',
                width: '100%',
                maxWidth: '400px',
                marginBottom: '20px',
                boxShadow: '0px 4px 8px rgba(0, 0, 0, 0.1)',
            }}>
                <h2 style={{ fontSize: '1.5rem', marginBottom: '15px' }}>Sign In</h2>
                <form onSubmit={handleLoginSubmit}>
                    <div style={{ marginBottom: '15px' }}>
                        <label htmlFor="username">Username:</label>
                        <input
                            type="text"
                            id="username"
                            name="username"
                            value={loginCredentials.username}
                            onChange={handleLoginChange}
                            style={{ width: '100%', padding: '8px', marginTop: '5px', borderRadius: '4px', border: '1px solid #ccc' }}
                        />
                    </div>
                    <div style={{ marginBottom: '15px' }}>
                        <label htmlFor="password">Password:</label>
                        <input
                            type="password"
                            id="password"
                            name="password"
                            value={loginCredentials.password}
                            onChange={handleLoginChange}
                            style={{ width: '100%', padding: '8px', marginTop: '5px', borderRadius: '4px', border: '1px solid #ccc' }}
                        />
                    </div>
                    <button type="submit" style={{
                        padding: '10px 20px',
                        borderRadius: '4px',
                        border: 'none',
                        backgroundColor: '#007bff',
                        color: '#fff',
                        cursor: 'pointer',
                        marginRight: '10px'
                    }}>
                        Login
                    </button>
                    <button type="button" onClick={handleCreateAccountClick} style={{
                        padding: '10px 20px',
                        borderRadius: '4px',
                        border: '1px solid #007bff',
                        backgroundColor: '#fff',
                        color: '#007bff',
                        cursor: 'pointer'
                    }}>
                        Create Account
                    </button>
                </form>
            </div>
        </div>
    );
};

export default LoginComponent;