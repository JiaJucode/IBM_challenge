'use client';

// import { useState } from 'react';
import { ThemeProvider } from '@mui/material/styles';
import ChatPage from './pages/chat_page';
import theme from './theme';

export default function Home() {
  return (
    <ThemeProvider theme={theme}>
      <ChatPage />
    </ThemeProvider>
  );
}
