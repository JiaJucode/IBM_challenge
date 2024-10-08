'use client';

// import { useState } from 'react';
import { ThemeProvider } from '@mui/material/styles';
import ChatPage from './pages/chat_page';
import theme from './theme';

export default function Home() {
  // const [message, setMessage] = useState('');

  // const fetchMessage = () => {
  //   fetch('http://localhost:5000/api/hello')  // Call the Flask backend
  //     .then(response => response.json())
  //     .then(data => setMessage(data.message))
  //     .catch(error => console.error('Error fetching message:', error));
  // };

  // return (
  //   <main>
  //     <h1>Frontend calling Backend</h1>
  //     <button onClick={fetchMessage}>Load Message</button>
  //     <p>Message from backend: {message}</p>
  //   </main>
  // );
  return (
    <ThemeProvider theme={theme}>
      <ChatPage />
    </ThemeProvider>
  );
}
