import * as React from 'react';
import Divider from '@mui/material/Divider';
import Drawer from '@mui/material/Drawer';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import HomeIcon from '@mui/icons-material/Home';
import DnsRoundedIcon from '@mui/icons-material/DnsRounded';
import PermMediaOutlinedIcon from '@mui/icons-material/PhotoSizeSelectActual';
import {LocationOn} from "@mui/icons-material";
import {Container, ListItemButton, makeStyles} from "@mui/material";
import Box from "@mui/material/Box";
import {Link} from "react-router-dom";

const categories = [
    {
        id: 'AngelBox Management',
        children: [
            {
                id: 'Location',
                icon: <LocationOn/>,
                link: '/location',
            },
            // {id: 'Database', icon: <DnsRoundedIcon/>},
            // {id: 'Storage', icon: <PermMediaOutlinedIcon/>}
        ],
    },
    // {
    //   id: 'Quality',
    //   children: [
    //     { id: 'Analytics', icon: <SettingsIcon /> },
    //     { id: 'Performance', icon: <TimerIcon /> },
    //     { id: 'Test Lab', icon: <PhonelinkSetupIcon /> },
    //   ],
    // },
];

const item = {
    py: '2px',
    px: 3,
    color: 'rgba(255, 255, 255, 0.7)',
    '&:hover, &:focus': {
        bgcolor: 'rgba(255, 255, 255, 0.08)',
    },
    width: '100%'
};

const itemCategory = {
    boxShadow: '0 -1px 0 rgb(255,255,255,0.1) inset',
    py: 1.5,
    px: 3,
};

export default function Navigator(props) {
    const {...other} = props;
    const { selected } = props;
    return (
        <Drawer variant="permanent" {...other}>
            <List disablePadding>
                <ListItem sx={{...item, ...itemCategory, fontSize: 22, color: '#fff'}}>
                    LoRa CMS
                </ListItem>
                <Link to='/' style={{textDecoration: 'none'}}>
                    <ListItem sx={{...item, ...itemCategory}}>
                        <ListItemIcon>
                            <HomeIcon/>
                        </ListItemIcon>
                        <ListItemText>Project Overview</ListItemText>
                    </ListItem>
                </Link>
                {categories.map(({id, children}) => (
                    <Box key={id} sx={{bgcolor: '#101F33', width: '100%'}}>
                        <ListItem sx={{py: 2, px: 3}}>
                            <ListItemText sx={{color: '#fff'}}>{id}</ListItemText>
                        </ListItem>
                        {children.map(({id: childId, icon, link}) => (
                            <ListItem disablePadding key={childId} sx={{width: '100%'}}>
                                <Link to={link} style={{textDecoration: 'none'}}>
                                    <ListItemButton sx={item}>
                                        <ListItemIcon>{icon}</ListItemIcon>
                                        <ListItemText>{childId}</ListItemText>
                                    </ListItemButton>
                                </Link>
                            </ListItem>
                        ))}

                        <Divider sx={{mt: 2}}/>
                    </Box>
                ))}
            </List>
        </Drawer>
    );
}