import React, { useState } from 'react';
import HWSets from './HWSets';
import { Button } from '@mui/material';

const ProjectNames = ({ projectName, isJoined }) => {
    const [joined, setJoined] = useState(isJoined);

    const toggleJoin = () => setJoined(!joined);

    return (
        <div style={{ border: '1px solid #ccc', margin: '10px 0', padding: '15px', borderRadius: '8px', backgroundColor: joined ? '#e0f7e9' : '#fff' }}>
            <h3>{projectName}</h3>
            <Button
                variant="contained"
                color={joined ? 'success' : 'primary'}
                onClick={toggleJoin}
                style={{ marginBottom: '10px' }}
            >
                {joined ? 'Leave' : 'Join'}
            </Button>
            <HWSets hwName="Hardware Set 1" />
            <HWSets hwName="Hardware Set 2" />
        </div>
    );
};

export default ProjectNames;
