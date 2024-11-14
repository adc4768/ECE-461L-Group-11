import React, { useState, useEffect } from 'react';
import ProjectNames from './ProjectNames'; // Assuming this component exists
import { Button, TextField, CircularProgress, Snackbar } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const Projects = () => {
    const navigate = useNavigate();
    const [projects, setProjects] = useState([]);
    const [newProjectName, setNewProjectName] = useState('');
    const [newProjectId, setNewProjectId] = useState('');
    const [joinProjectId, setJoinProjectId] = useState(''); // New state for joining a project
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    useEffect(() => {
        fetchUserProjects();
    }, []);

    const fetchUserProjects = async () => {
        const userId = sessionStorage.getItem('userId');
        if (!userId) {
            alert('User not logged in');
            return;
        }
        setLoading(true);
        try {
            const response = await axios.get(`http://localhost:5000/get_user_projects?userId=${userId}`);
            if (response.status === 200 && response.data.joiningPJ) {
                const fetchedProjects = response.data.joiningPJ.map((projectName) => ({
                    name: projectName,
                    isJoined: true,
                    projectId: projectName
                }));
                setProjects(fetchedProjects);
            } else {
                setProjects([]);
            }
        } catch (error) {
            setError('Error fetching user projects');
        }
        setLoading(false);
    };

    const addProject = async () => {
        if (newProjectName.trim() === '' || newProjectId.trim() === '') {
            setError('Please enter both a project name and project ID.');
            return;
        }
        const userId = sessionStorage.getItem('userId');
        if (!userId) {
            setError('User not logged in');
            return;
        }
        setLoading(true);
        try {
            const projectResponse = await axios.post('http://localhost:5000/create_project', {
                userId: userId,
                projectName: newProjectName,
                projectId: newProjectId,
                description: 'Some project description'
            });
            if (projectResponse.status === 200) {
                const userResponse = await axios.post('http://localhost:5000/join', {
                    projectId: newProjectId,
                    userId: userId
                });
                if (userResponse.status === 200) {
                    setNewProjectName('');
                    setNewProjectId('');
                    fetchUserProjects();
                } else {
                    setError(userResponse.data.message);
                }
            }
        } catch (error) {
            setError('Failed to create project or update user access. Please try again.');
        }
        setLoading(false);
    };

    const joinProject = async () => {
        if (joinProjectId.trim() === '') {
            setError('Please enter a project ID to join.');
            return;
        }
        const userId = sessionStorage.getItem('userId');
        if (!userId) {
            setError('User not logged in');
            return;
        }
        setLoading(true);
        try {
            const response = await axios.post('http://localhost:5000/join', {
                userId: userId,
                projectId: joinProjectId
            });
            if (response.status === 200) {
                setJoinProjectId('');
                fetchUserProjects(); // Refresh project list on successful join
            } else {
                setError(response.data.message);
            }
        } catch (error) {
            setError('Failed to join project. Please try again.');
        }
        setLoading(false);
    };

    const handleLogout = () => {
        sessionStorage.removeItem('userId');
        navigate('/');
    };

    return (
        <div style={{ padding: '20px', maxWidth: '600px', margin: 'auto', position: 'relative', minHeight: '100vh' }}>
            <h1>Projects</h1>
            {loading ? (
                <CircularProgress />
            ) : (
                <div style={{ border: '1px solid #ddd', padding: '20px', borderRadius: '8px', backgroundColor: '#f9f9f9', maxHeight: '500px', overflowY: 'auto' }}>
                    {projects.map((project, index) => (
                        <ProjectNames key={index} projectName={project.name} isJoined={project.isJoined} projectId={project.projectId} />
                    ))}
                </div>
            )}
            <div style={{ marginTop: '20px', display: 'flex', flexDirection: 'column', gap: '10px' }}>
                <TextField label="New Project Name" variant="outlined" value={newProjectName} onChange={(e) => setNewProjectName(e.target.value)} fullWidth />
                <TextField label="New Project ID" variant="outlined" value={newProjectId} onChange={(e) => setNewProjectId(e.target.value)} fullWidth />
                <Button variant="contained" onClick={addProject} color="primary" disabled={loading}>
                    {loading ? 'Adding...' : 'Add Project'}
                </Button>
            </div>
            <div style={{ marginTop: '20px', display: 'flex', flexDirection: 'column', gap: '10px' }}>
                <TextField label="Project ID to Join" variant="outlined" value={joinProjectId} onChange={(e) => setJoinProjectId(e.target.value)} fullWidth />
                <Button variant="contained" onClick={joinProject} color="secondary" disabled={loading}>
                    {loading ? 'Joining...' : 'Join Project'}
                </Button>
            </div>
            <Button variant="contained" style={{ backgroundColor: 'red', color: '#fff', position: 'absolute', bottom: '20px', right: '20px' }} onClick={handleLogout}>
                Logout
            </Button>
            <Snackbar open={!!error} autoHideDuration={6000} onClose={() => setError('')} message={error} />
        </div>
    );
};

export default Projects;
