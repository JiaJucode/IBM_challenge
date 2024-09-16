import React from 'react';
import { useState, useEffect, useRef } from 'react';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid2';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import AssistantIcon from '@mui/icons-material/Assistant';
import {IconButton, InputAdornment, TextField } from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';

const exampleChat = {
    name: "example",
    messages: [
        "questions",
        `blablbalsdfl absldfblab sl fbalsfbflabs ldffblabs dflbas fhjkasdf kjj askdf hjk sahkjf gasdgf
        blablbals dflabsl dfblabslfbal sfbfl absldf fblabsd flbasfh jkasdf kjjas dfhjksah kjfgasdgf
        blablbals dflabsldf blab slfbalsf bflabsldffblab sdflb asf hjka sdfkjjaskdf hjksa hkjfgasdgf
        blablbalsdf labsldf blabslfbalsf bflabsldffblabsdflbasfhjkasdfkjjas kdfhj ksahkjfgasdgf
        blablbalsdflabsldfbl absl fbalsfbflabsldff blabsdflbasfhj kas dfkjjas kdfhjksah kjfgasdgf
        blablbal sdfl absldfblab slfbalsfbflabsl ff blabsdflb asfh jkasdfkjjaskdfhjk sahkjfgasdgf`,
        "questions",
        `blablbalsdfl absldfblab sl fbalsfbflabs ldffblabs dflbas fhjkasdf kjj askdf hjk sahkjf gasdgf
        blablbals dflabsl dfblabslfbal sfbfl absldf fblabsd flbasfh jkasdf kjjas dfhjksah kjfgasdgf
        blablbals dflabsldf blab slfbalsf bflabsldffblab sdflb asf hjka sdfkjjaskdf hjksa hkjfgasdgf
        blablbalsdf labsldf blabslfbalsf bflabsldffblabsdflbasfhjkasdfkjjas kdfhj ksahkjfgasdgf
        blablbalsdflabsldfbl absl fbalsfbflabsldff blabsdflbasfhj kas dfkjjas kdfhjksah kjfgasdgf
        blablbal sdfl absldfblab slfbalsfbflabsl ff blabsdflb asfh jkasdfkjjaskdfhjk sahkjfgasdgf`,
        "questions",
        `blablbalsdfl absldfblab sl fbalsfbflabs ldffblabs dflbas fhjkasdf kjj askdf hjk sahkjf gasdgf
        blablbals dflabsl dfblabslfbal sfbfl absldf fblabsd flbasfh jkasdf kjjas dfhjksah kjfgasdgf
        blablbals dflabsldf blab slfbalsf bflabsldffblab sdflb asf hjka sdfkjjaskdf hjksa hkjfgasdgf
        blablbalsdf labsldf blabslfbalsf bflabsldffblabsdflbasfhjkasdfkjjas kdfhj ksahkjfgasdgf
        blablbalsdflabsldfbl absl fbalsfbflabsldff blabsdflbasfhj kas dfkjjas kdfhjksah kjfgasdgf
        blablbal sdfl absldfblab slfbalsfbflabsl ff blabsdflb asfh jkasdfkjjaskdfhjk sahkjfgasdgf`,
        "questions",
        `blablbalsdfl absldfblab sl fbalsfbflabs ldffblabs dflbas fhjkasdf kjj askdf hjk sahkjf gasdgf
        blablbals dflabsl dfblabslfbal sfbfl absldf fblabsd flbasfh jkasdf kjjas dfhjksah kjfgasdgf
        blablbals dflabsldf blab slfbalsf bflabsldffblab sdflb asf hjka sdfkjjaskdf hjksa hkjfgasdgf
        blablbalsdf labsldf blabslfbalsf bflabsldffblabsdflbasfhjkasdfkjjas kdfhj ksahkjfgasdgf
        blablbalsdflabsldfbl absl fbalsfbflabsldff blabsdflbasfhj kas dfkjjas kdfhjksah kjfgasdgf
        blablbal sdfl absldfblab slfbalsfbflabsl ff blabsdflb asfh jkasdfkjjaskdfhjk sahkjfgasdgf`,
        "questions",
        `blablbalsdfl absldfblab sl fbalsfbflabs ldffblabs dflbas fhjkasdf kjj askdf hjk sahkjf gasdgf
        blablbals dflabsl dfblabslfbal sfbfl absldf fblabsd flbasfh jkasdf kjjas dfhjksah kjfgasdgf
        blablbals dflabsldf blab slfbalsf bflabsldffblab sdflb asf hjka sdfkjjaskdf hjksa hkjfgasdgf
        blablbalsdf labsldf blabslfbalsf bflabsldffblabsdflbasfhjkasdfkjjas kdfhj ksahkjfgasdgf
        blablbalsdflabsldfbl absl fbalsfbflabsldff blabsdflbasfhj kas dfkjjas kdfhjksah kjfgasdgf
        blablbal sdfl absldfblab slfbalsfbflabsl ff blabsdflb asfh jkasdfkjjaskdfhjk sahkjfgasdgf`,
        "questions",
        `blablbalsdfl absldfblab sl fbalsfbflabs ldffblabs dflbas fhjkasdf kjj askdf hjk sahkjf gasdgf
        blablbals dflabsl dfblabslfbal sfbfl absldf fblabsd flbasfh jkasdf kjjas dfhjksah kjfgasdgf
        blablbals dflabsldf blab slfbalsf bflabsldffblab sdflb asf hjka sdfkjjaskdf hjksa hkjfgasdgf
        blablbalsdf labsldf blabslfbalsf bflabsldffblabsdflbasfhjkasdfkjjas kdfhj ksahkjfgasdgf
        blablbalsdflabsldfbl absl fbalsfbflabsldff blabsdflbasfhj kas dfkjjas kdfhjksah kjfgasdgf
        blablbal sdfl absldfblab slfbalsfbflabsl ff blabsdflb asfh jkasdfkjjaskdfhjk sahkjfgasdgf`,
    ]
}

const ChatPage = () => {
    const [chatBoxs, setChatBoxs] = useState([exampleChat]);
    const [currentChat, setCurrentChat] = useState(exampleChat);
    const [message, setMessage] = useState('');
    const chatBottomRef = useRef<HTMLDivElement>(null);
    const [replyWaiting, setReplyWaiting] = useState(false);

    useEffect(() => {
        // fetch and setCHatBoxs
    }, []);

    useEffect(() => {
        chatBottomRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [currentChat]);

    useEffect(() => {
        if (replyWaiting) {
            // fake bot reply
            setTimeout(() => {
                const newMessage = {
                    sender: '',
                    message: 'I am a bot',
                }
                setCurrentChat({
                    name: currentChat.name,
                    messages: [...currentChat.messages, newMessage]
                });
                setReplyWaiting(false);
            }, 1000);
        }
    }, [replyWaiting]);

    const sendRequest = () => {
        // update backend with the new message

        // update frontend
        const newMessage = {
            sender: 'user',
            message: message,
        }
        setCurrentChat({
            name: currentChat.name,
            messages: [...currentChat.messages, newMessage]
        });
        setReplyWaiting(true);
    }

    const handleKeyDown = (event: React.KeyboardEvent<HTMLDivElement>) => {
        if (event.key === 'Enter' && message.length && !event.shiftKey && !event.ctrlKey) {
            sendRequest();
            setMessage('');
            event.preventDefault()
        }
    }

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
                            backgroundColor: 'primary.main',
                            width: '100%',
                            height: '100dvh',
                            paddingBottom: 7,
                            overflowY: 'auto'
                        }}>
                        <Stack spacing={2} direction="column" alignItems="center">
                            {currentChat.messages.map((message, index) => (
                                <Box
                                    key={index}
                                    sx={{
                                        justifyContent: index % 2 === 0 ? 'flex-end' : 'flex-start',
                                        display: 'flex',
                                        width: '70%',
                                        padding: 2,
                                    }}
                                >
                                    {index % 2 === 1 ? (
                                        <AssistantIcon sx={{marginLeft:'-5%', padding:1, fontSize:50}}/>
                                    ) : null}
                                    <Typography variant='h5'>
                                        {message.message}
                                    </Typography>
                                </Box>
                            ))}
                        </Stack>
                        <div ref={chatBottomRef} />
                        <TextField variant='outlined' multiline fullWidth value={message} 
                            disabled={replyWaiting}
                            onKeyDown={(e) => handleKeyDown(e)}
                            onChange={(e) => setMessage(e.target.value)}
                            slotProps={{
                                input: {
                                    endAdornment: (
                                    <InputAdornment position="end">
                                        <IconButton onClick={sendRequest}>
                                            <SearchIcon sx={{ color: 'white' }}/>
                                        </IconButton>
                                    </InputAdornment>
                                    )
                                }
                            }}
                            sx={{
                                position: 'fixed',
                                bottom: 10, width: '60%',
                                justifyContent: 'center',
                                opacity: 0.99,
                                marginLeft: '10%',
                                borderRadius: 7,
                                backgroundColor: 'primary.light',
                                alignItems: 'center',
                                '& .MuiInputBase-input': {
                                    fontSize: 25, // Apply font size to the input text
                                },
                                '& .MuiOutlinedInput-root.Mui-disabled': {
                                    backgroundColor: 'primary.main',
                                    borderRadius: 7,
                                }
                            }}/>
                        <InputAdornment position="end">
                            <IconButton>
                                <SearchIcon />
                            </IconButton>
                        </InputAdornment>
                    </Box>

                </Grid>
            </Grid>
        </div>
    );
}

export default ChatPage;