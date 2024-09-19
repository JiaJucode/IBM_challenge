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
        // Fetch chat list from backend
        fetch('http://localhost:5000/api/chats')
            .then(response => response.json())
            .then((data: { id: number; search_query: string; summarized_search_results: string }[]) => {
                let tempChatBoxs: {[id: number]: ChatBox} = {};
                data.forEach((chat) => {
                    tempChatBoxs = {
                        ...tempChatBoxs,
                        [chat.id]: {
                            name: chat.search_query,
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
            if (currentChat !== null) {
                if (chatBoxs[currentChat].messages.length === 0) {
                    // Fetch chat messages for the selected chat
                    fetch(`http://localhost:5000/api/chat/${currentChat}`)
                        .then(response => response.json())
                        .then((data: { chat: { search_query: string }; messages: { role: string; content: string }[] }) => {
                            if (data.messages.length > 0) {
                                setChatBoxs((prevChatBoxs) => {
                                    prevChatBoxs[currentChat].messages = data.messages.map(m => m.content);
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
        if (!replyWaiting) {
            chatBottomRef.current?.scrollIntoView({ behavior: 'smooth' });
        }
    }, [replyWaiting]);

    const handleSelectChat = (chatID: number) => {
        setCurrentChat(chatID);
        setChatMessagesLoading(true);
    }

    const sendRequest = () => {
        setReplyWaiting(true);
        if (currentChat !== null) {
            setChatBoxs((prevChatBoxs) => {
                const newChatBoxs = prevChatBoxs;
                newChatBoxs[currentChat].messages.push(message);
                return newChatBoxs;
            });
        }

        // Send the new message to backend and get AI response
        fetch('http://localhost:5000/api/ai_response', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                chat_id: currentChat,  // Updated key to match backend
                message: message
            })
        }).then(response => response.json())
            .then((data: { response: string }) => {
                if (data.response.length > 0 && currentChat !== null) {
                    setChatBoxs((prevChatBoxs) => {
                        const newChatBoxs = prevChatBoxs;
                        newChatBoxs[currentChat].messages.push(data.response);
                        return newChatBoxs;
                    });
                }
                setReplyWaiting(false);
            })
            .catch((error) => {
                console.error('Error:', error);
                setReplyWaiting(false);
            });
    }

    const handleKeyDown = (event: React.KeyboardEvent<HTMLDivElement>) => {
        if (event.key === 'Enter' && message.length && !event.shiftKey && !event.ctrlKey) {
            sendRequest();
            setMessage('');
            event.preventDefault();
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
                                    <Button sx={{ width: '100%' }} onClick={() => handleSelectChat(Number(chatID))}>
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
                        sx={{
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
                                                <AssistantIcon sx={{ marginLeft: '-5%', padding: 1, fontSize: 50 }} />
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
                                    InputProps={{
                                        endAdornment: (
                                            <InputAdornment position="end">
                                                <IconButton onClick={sendRequest}>
                                                    <SearchIcon sx={{ color: 'white' }} />
                                                </IconButton>
                                            </InputAdornment>
                                        )
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
                            </div>
                        : null}
                    </Box>
                </Grid>
            </Grid>
        </div>
    );
}

export default ChatPage;
