import React from 'react';
import ProjectNames from './ProjectNames';
import { Button } from '@mui/material';
import { useNavigate } from 'react-router-dom';

const Projects = () => {
    const navigate = useNavigate();

    const handleLogout = () => {
        navigate('/');
    };

    return (
        <div style={{ padding: '20px', maxWidth: '600px', margin: 'auto', position: 'relative', minHeight: '100vh' }}>
            <h1>Projects</h1>
            <div style={{ border: '1px solid #ddd', padding: '20px', borderRadius: '8px', backgroundColor: '#f9f9f9' }}>
                <ProjectNames projectName="Project Name 1" isJoined={false} />
                <ProjectNames projectName="Project Name 2" isJoined={true} />
                <ProjectNames projectName="Project Name 3" isJoined={false} />
            </div>
            <Button
                variant="contained"
                style={{
                    backgroundColor: 'red',
                    color: '#fff',
                    position: 'absolute',
                    bottom: '20px',
                    right: '20px',
                }}
                onClick={handleLogout}
            >
                Logout
            </Button>
        </div>
    );
};

export default Projects;
