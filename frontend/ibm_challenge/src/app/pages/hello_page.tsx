import React from 'react';
import { useState, useEffect } from 'react';
import Grid from '@mui/material/Grid2';
import { Box, Typography, TextField, InputAdornment, IconButton } from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';

const Home = () => {
    const [message, setMessage] = useState('');
    const [titles, setTitles] = useState<string[]>([]);
    const [titlesLoaded, setTitlesLoaded] = useState(false);

    useEffect(() => {
        fetch('http://localhost:5000/api/hello')
            .then(response => response.json())
            .then((data: {chats: {id: number, title: string}[]}) => {
                console.log(data);
                const titles: string[] = data.chats.map((item) => item.title, []);
                setTitles(titles);
                setTitlesLoaded(true);
            }
        );
    }, []);

    const sendRequest = () => {
    }

    const handleKeyDown = (event: React.KeyboardEvent<HTMLDivElement>) => {
        if (event.key === 'Enter' && message.length && !event.shiftKey && !event.ctrlKey) {
            sendRequest();
            setMessage('');
            event.preventDefault();
        }
    }


    return (
        <Box sx={{
            display: 'flex',
            width: '100%',
            alignContent: 'center',
            justifyContent: 'center',
        }}>
            {titlesLoaded ?
            <Grid container spacing={2} direction="row" marginTop={20} padding={2}
                sx={{
                    alignContent: 'center',
                    justifyContent: 'center',
                    backgroundColor: 'primary.main',
                    borderRadius: 10,
                }}>
                <Grid size={10}>
                    <Box sx={{ 
                        justifyContent: 'center',
                        alignItems: 'center',
                        }}>
                        <Typography variant="h4" align='center'>
                            Hello! What would you like to search?
                        </Typography>
                    </Box>
                </Grid>
                <Grid size={8}>
                    <Box sx={{ 
                        flexGrow: 1,
                        justifyContent: 'center',
                        alignItems: 'center',
                        backgroundColor: 'primary.main',
                        }}>
                        <TextField variant='outlined' multiline fullWidth value={message} 
                            onKeyDown={(e) => handleKeyDown(e)}
                            onChange={(e) => setMessage(e.target.value)}
                            InputProps={{
                                endAdornment: (
                                    <InputAdornment position="end">
                                        <IconButton onClick={sendRequest}>
                                            <SearchIcon sx={{ color: 'white' }} onClick={sendRequest} />
                                        </IconButton>
                                    </InputAdornment>
                                )
                            }}
                            sx={{
                                justifyContent: 'center',
                                opacity: 0.99,
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
                    </Box>
                </Grid>
                {titles.map((title, index) => (
                    <Grid size={8} key={index}>
                        <Typography variant="h5" align='center'>
                            {title}
                        </Typography>
                    </Grid>
                ))}
            </Grid>
            :
            <Typography variant="h4" align='center'>
                Loading...
            </Typography>
            }
        </Box>
        );
};

export default Home;