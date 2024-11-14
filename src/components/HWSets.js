import React, { useState } from 'react';
import { Button, TextField } from '@mui/material';

const HWSets = ({ hwName }) => {
    const [quantity, setQuantity] = useState(0);

    const handleCheckIn = () => alert(`${quantity} units checked in.`);
    const handleCheckOut = () => alert(`${quantity} units checked out.`);

    return (
        <div style={{ marginTop: '10px' }}>
            <h4>{hwName}</h4>
            <TextField
                label="Quantity"
                type="number"
                variant="outlined"
                value={quantity}
                onChange={(e) => setQuantity(e.target.value)}
                size="small"
                style={{ marginRight: '10px', width: '80px' }}
            />
            <Button
                variant="outlined"
                color="secondary"
                onClick={handleCheckOut}
                style={{ marginRight: '5px', borderColor: 'black', color: 'black' }}
            >
                Check Out
            </Button>
            <Button
                variant="outlined"
                color="primary"
                onClick={handleCheckIn}
                style={{ borderColor: 'black', color: 'black' }}
            >
                Check In
            </Button>
        </div>
    );
};

export default HWSets;
