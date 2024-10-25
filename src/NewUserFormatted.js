import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom'; 

const NewUserFormatted = () => {
    const navigate = useNavigate(); 
    const [inputValueUser, setInputValueUser] = useState('');
    const [inputValuePass, setInputValuePass] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        alert(inputValueUser + inputValuePass);
    };

    const handleChangeUser = (e) => {
        setInputValueUser(e.target.value);
    };
    const handleChangePass = (e) => {
        setInputValuePass(e.target.value);
    };

    const signInPage = () => {
        navigate('/'); 
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
            <h1 style={{ fontSize: '2rem', fontWeight: 'bold', marginBottom: '20px' }}>New User</h1>

            <div style={{
                border: '1px solid #ddd',
                borderRadius: '8px',
                padding: '20px',
                width: '100%',
                maxWidth: '400px',
                marginBottom: '20px',
                boxShadow: '0px 4px 8px rgba(0, 0, 0, 0.1)',
            }}>
                <h2 style={{ fontSize: '1.5rem', marginBottom: '15px' }}>Sign Up</h2>
                <div style={{ marginBottom: '15px'}}>
                    Username:
                    <input
                        type="text"
                        value={inputValueUser}
                        name="username"
                        onChange={handleChangeUser}
                        style={{ width: '100%', padding: '8px', marginTop: '5px', borderRadius: '4px', border: '1px solid #ccc' }}
                    />
                </div>
                <div style = {{marginBottom: '15px'}}>
                    Password:
                    <input
                        type="text"
                        value={inputValuePass}
                        name="password"
                        onChange={handleChangePass}
                        style={{ width: '100%', padding: '8px', marginTop: '5px', borderRadius: '4px', border: '1px solid #ccc' }}
                    />
                </div>
                <div style={{ padding: '10px' }}>
                    <input
                        type="button"
                        value="Submit"
                        onClick={handleSubmit}
                    />
                </div>
                <div style={{ marginTop: '40px', fontSize: '.75rem' }}>
                    Have an account? <span onClick={signInPage} style={{ color: 'blue', cursor: 'pointer', textDecoration: 'underline'}}>Sign in</span>
                </div></div>

        </div>
    )
}

export default NewUserFormatted