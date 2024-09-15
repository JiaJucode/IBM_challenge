import React from 'react';
import { useState, useEffect } from 'react';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid2';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import AssistantIcon from '@mui/icons-material/Assistant';

const exampleChat = {
    name: "example",
    messages: [
        {
            sender: "user",
            message: "questions",
        },
        {
            sender: '',
            message: `blablbalsdfl absldfblab sl fbalsfbflabs ldffblabs dflbas fhjkasdf kjj askdf hjk sahkjf gasdgf
            blablbals dflabsl dfblabslfbal sfbfl absldf fblabsd flbasfh jkasdf kjjas dfhjksah kjfgasdgf
            blablbals dflabsldf blab slfbalsf bflabsldffblab sdflb asf hjka sdfkjjaskdf hjksa hkjfgasdgf
            blablbalsdf labsldf blabslfbalsf bflabsldffblabsdflbasfhjkasdfkjjas kdfhj ksahkjfgasdgf
            blablbalsdflabsldfbl absl fbalsfbflabsldff blabsdflbasfhj kas dfkjjas kdfhjksah kjfgasdgf
            blablbal sdfl absldfblab slfbalsfbflabsl ff blabsdflb asfh jkasdfkjjaskdfhjk sahkjfgasdgf`,
        }, 
    ]
}

const ChatPage = () => {
    const [chatBoxs, setChatBoxs] = useState([exampleChat]);
    const [currentChat, setCurrentChat] = useState(exampleChat);

    useEffect(() => {
        // fetch shits
    }, []);

    return (
        <div>
            <Grid container spacing={1} sx={{ width: '100%', height: '100%' }}>
                <Grid key={"names"} size={2}>
                    <Box
                        sx={{
                        backgroundColor: 'primary.dark',
                        width: '100%',
                        height: '100dvh',
                        }}
                    >
                        <Grid container spacing={2} direction="column" alignItems="center" padding={1} 
                            sx={{ width: '100%', height: '100%' }}>
                            {chatBoxs.map((chat, index) => (
                                <Grid key={index} size={12} sx={{ width: '100%' }}>
                                    <Button sx={{ width: '100%'}} onClick={() => setCurrentChat(chat)}>
                                        <Typography variant="h5" sx={{ textAlign: 'center' }} color='text.primary'>
                                            {chat.name}
                                        </Typography>
                                    </Button>
                                </Grid>
                            ))}
                        </Grid>
                    </Box>
                </Grid>
                <Grid key={"contents"} size={10}>
                    <Box
                        sx = {{
                            width: '100%',
                            height: '100dvh',
                            overflowY: 'auto'
                        }}>
                        <Stack spacing={2} direction="column" alignItems="center">
                            {currentChat.messages.map((message, index) => (
                                <Box
                                    key={index}
                                    sx={{
                                        justifyContent: message.sender.length === 0 ? 'left' : 'right',
                                        display: 'flex',
                                        width: '70%',
                                        padding: 2,
                                    }}
                                >
                                    {message.sender.length === 0 ? (
                                        <AssistantIcon sx={{marginLeft:'-5%', padding:1, fontSize:50}}/>
                                    ) : null}
                                    <Typography variant='h5'>
                                        {message.message}
                                    </Typography>
                                </Box>
                            ))}
                        </Stack>
                    </Box>
                </Grid>
            </Grid>
        </div>
    );
}

export default ChatPage;