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

interface ChatBox {
    name: string;
    messages: string[];
}

const ChatPage = () => {
    const [chatBoxs, setChatBoxs] = useState<{[id: number]: ChatBox}>({});
    const [currentChat, setCurrentChat] = useState<number | null>(null);
    const [message, setMessage] = useState('');
    const chatBottomRef = useRef<HTMLDivElement>(null);
    const [replyWaiting, setReplyWaiting] = useState(false);
    const [chatListLoading, setChatListLoading] = useState(true);
    const [chatMessagesLoading, setChatMessagesLoading] = useState(false);

    useEffect(() => {
        // fetch and setCHatBoxs
        console.log('fetching chat lists');
        fetch('http://localhost:5000/api/ChatHistory?user_ID=1')
            .then(response => response.json())
            .then((data: { chat_ID: number; chat_name: string }[]) => {
                let tempChatBoxs: {[id: number]: ChatBox} = {};
                data.forEach((chat) => {
                    tempChatBoxs = {
                        ...tempChatBoxs,
                        [chat.chat_ID]: {
                            name: chat.chat_name,
                            messages: []
                        }
                    }
                });
                setChatBoxs(tempChatBoxs);
                setChatListLoading(false);
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    }, []);

    useEffect(() => {
        if (!chatMessagesLoading) {
            chatBottomRef.current?.scrollIntoView({ behavior: 'smooth' });
        }
        else {
            console.log(currentChat);
            if (currentChat !== null) {
                console.log('currentChat:', currentChat);
                if (chatBoxs[currentChat].messages.length === 0) {
                    // fetch and set messages
                    console.log('fetching chat messages');
                    fetch(`http://localhost:5000/api/ChatHistory?chat_ID=${currentChat}`)
                        .then(response => response.json())
                        .then((data: { chat_history: string }) => {
                            if (chatBoxs[currentChat].messages.length === 0 && data.chat_history.length > 0) {
                                setChatBoxs((prevChatBoxs) => {
                                    prevChatBoxs[currentChat].messages = JSON.parse(data.chat_history);
                                    return prevChatBoxs;
                                });
                                setChatMessagesLoading(false);
                            }
                        })
                        .catch((error) => {
                            console.error('Error:', error);
                        });
                }
            }
        }
    }, [chatMessagesLoading]);

    useEffect(() => {
        if (replyWaiting) {
            // fake bot reply
            
        }
    }, [replyWaiting]);

    const handleSelectChat = (chatID: number) => {
        console.log('selecting chat:', chatID);
        setCurrentChat(chatID);
        setChatMessagesLoading(true);
    }

    const sendRequest = () => {
        // update backend with the new message

        // update frontend
        if (currentChat !== null) {
            setChatBoxs((prevChatBoxs) => {
                let newChatBoxs = prevChatBoxs;
                newChatBoxs[currentChat].messages.push(message);
                return newChatBoxs;
            });
        }
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
                        {!chatListLoading ?
                        <Grid container spacing={2} direction="column" alignItems="center" padding={1} 
                            sx={{ width: '100%', height: '100%' }}>
                            {Object.keys(chatBoxs).map((chatID: string) => (
                                <Grid key={chatID} size={12} sx={{ width: '100%' }}>
                                    <Button sx={{ width: '100%'}} onClick={() => handleSelectChat(Number(chatID))}>
                                        <Typography variant="h5" sx={{ textAlign: 'center' }} color='text.primary'>
                                            {chatBoxs[Number(chatID)].name}
                                        </Typography>
                                    </Button>
                                </Grid>
                            ))}
                        </Grid>
                        : null}
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
                            {currentChat !== null && !chatMessagesLoading ?
                                <div>
                                    <Stack spacing={2} direction="column" alignItems="center">
                                        {chatBoxs[currentChat].messages.map((message, index) => (
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
                                                    {message}
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
                                </div>
                            : null}
                        </Box>

                    </Grid>
            </Grid>
        </div>
    );
}

export default ChatPage;