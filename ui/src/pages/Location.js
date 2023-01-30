import * as React from 'react';
import {Container} from "@mui/material";
import Paper from "@mui/material/Paper";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";
import MapView from "../components/Map";

function Location({serverApi}) {
    const fakePayload = serverApi.getBoxesLocation()
    return (
        <Container sx={{display: 'flex'}} maxWidth='100%'>
            <div className='map-container'><MapView sensors={fakePayload}/></div>
            <div className='control-container'>
                {fakePayload.map(({id, color, timestamp}) => (
                    <Paper key={id} sx={{m: 1.5}}>
                        <Box p={1}>
                            <Typography variant="h6" sx={{display: 'flex'}}>
                                <div style={{backgroundColor: color, width: '30px', borderRadius:'15px', marginRight: '10px'}}></div>
                                <div>Box {id}</div>
                            </Typography>
                            <Typography variant="p">Last Updated: {timestamp} </Typography>
                        </Box>
                    </Paper>
                ))}

            </div>
        </Container>
    )
}

export default Location;
