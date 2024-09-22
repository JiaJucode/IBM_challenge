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

// TODO create default new chat page

const ChatPage = () => {
    const [chatBoxs, setChatBoxs] = useState<{[id: number]: ChatBox}>({});
    const [currentChat, setCurrentChat] = useState<number>(-1);
    const [message, setMessage] = useState('');
    const chatBottomRef = useRef<HTMLDivElement>(null);
    const [replyWaiting, setReplyWaiting] = useState(false);
    const [chatListLoading, setChatListLoading] = useState(true);
    const [chatMessagesLoading, setChatMessagesLoading] = useState(false);

    useEffect(() => {
        // Fetch chat list from backend
        fetch('http://localhost:5000/api/hello')
            .then(response => response.json())
            .then((data: {chats: { chat_id: number; title: string}[]}) => {
                console.log(data);
                if (data.chats.length !== 0) {
                    setChatBoxs((prevChatBoxs) => {
                        const newChatBoxs = prevChatBoxs;
                        data.chats.forEach((chat) => {
                            newChatBoxs[chat.chat_id] = {
                                name: chat.title,
                                messages: []
                            };
                        });
                        return newChatBoxs;
                    });
                }
                console.log(chatBoxs);
                setChatListLoading(false);
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    }, [chatBoxs]);

    useEffect(() => {
        if (!chatMessagesLoading) {
            chatBottomRef.current?.scrollIntoView({ behavior: 'smooth' });
        }
        else {
            if (currentChat !== -1) {
                if (chatBoxs[currentChat].messages.length === 0) {
                    // Fetch chat messages for the selected chat
                    console.log("fetching chat messages for chat id: " + currentChat);
                    fetch(`http://localhost:5000/api/chat?chat_id=${currentChat}`)
                        .then(response => response.json())
                        .then((data: {content: string, role: string}[]) => {
                            console.log(data);
                            setChatBoxs((prevChatBoxs) => {
                                const newChatBoxs = prevChatBoxs;
                                newChatBoxs[currentChat].messages = data.map((message) => message.content);
                                return newChatBoxs;
                            });
                            setChatMessagesLoading(false);
                        })
                        .catch((error) => {
                            console.error('Error:', error);
                            setChatMessagesLoading(false);
                        });
                }
                else {
                    setChatMessagesLoading(false);
                }
            }
        }
    }, [chatMessagesLoading, chatBoxs, currentChat]);

    useEffect(() => {
        if (!replyWaiting) {
            chatBottomRef.current?.scrollIntoView({ behavior: 'smooth' });
        }
    }, [replyWaiting]);

    const handleSelectChat = (chatID: number) => {
        if (chatID < -1) {
            console.log("selected chat id is invalid");
        }
        else {
            setCurrentChat(chatID);
            setChatMessagesLoading(chatID !== -1);
        }
    }

    const sendRequest = () => {
        setReplyWaiting(true);

        if (currentChat === -1) {
            // send /api/start request
            fetch('http://localhost:5000/api/start', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    initial_message: message
                })
            }).then(response => response.json())
                .then((data: { chat_id: number, title: string, response: string}) => {
                    if (data.response.length > 0) {
                        setChatBoxs((prevChatBoxs) => {
                            const newChatBoxs = prevChatBoxs;
                            newChatBoxs[data.chat_id] = {
                                name: data.title,
                                messages: [message, data.response]
                            };
                            return newChatBoxs;
                        });
                        setCurrentChat(data.chat_id);
                    }
                    setReplyWaiting(false);
                })
        }
        else {
            setChatBoxs((prevChatBoxs) => {
                const newChatBoxs = prevChatBoxs;
                newChatBoxs[currentChat].messages.push(message);
                return newChatBoxs;
            });

            // send /api/ai_response request
            fetch('http://localhost:5000/api/ai_response', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    chat_id: currentChat,
                    message: message
                })
            }).then(response => response.json())
                .then((data: { response: string }) => {
                    if (data.response.length > 0 && currentChat !== -1) {
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
                        <Grid container spacing={2} direction="column" alignItems="center" padding={1} 
                            sx={{ width: '100%', height: '100%' }}>
                            <Grid key={-1} size={12} sx={{ width: '100%' }}>
                                <Button sx={{ width: '100%' }} onClick={() => handleSelectChat(-1)}>
                                    <Typography sx={{ textAlign: 'center', 
                                                    fontSize: '30px', 
                                                    textTransform: 'none', 
                                                    whiteSpace: 'nowrap',
                                                    overflow: 'hidden',
                                                    textOverflow: 'ellipsis',
                                            }} color='text.primary'>
                                        New chat
                                    </Typography>
                                </Button>
                            </Grid>
                            {!chatListLoading ?
                                Object.keys(chatBoxs).map((chatID: string) => (
                                    <Grid key={chatID} size={12} sx={{ width: '100%' }}>
                                        <Button sx={{ width: '100%' }} onClick={() => handleSelectChat(Number(chatID))}>
                                            <Typography 
                                                sx={{ textAlign: 'center', 
                                                    fontSize: '30px', 
                                                    textTransform: 'none', 
                                                    whiteSpace: 'nowrap',
                                                    overflow: 'hidden',
                                                    textOverflow: 'ellipsis',
                                            }} color='text.primary'>
                                                {chatBoxs[Number(chatID)].name}
                                            </Typography>
                                        </Button>
                                    </Grid>)
                                )
                            : null}
                        </Grid>
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
                        {!chatMessagesLoading ?
                            <div>
                                <Stack spacing={2} direction="column" alignItems="center">
                                    {currentChat !== -1 ?
                                        chatBoxs[currentChat].messages.map((message, index) => (
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
                                            ))
                                    : 
                                    <Box
                                        sx={{
                                            justifyContent: 'center',
                                            display: 'flex',
                                            padding: 2
                                        }}>  
                                        <Typography variant="h3" align='center' sx={{ paddingTop: "50%"}}>
                                            {!replyWaiting ? "Hello! What would you like to search?" : "Loading response..."}
                                        </Typography>
                                    </Box>}
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
