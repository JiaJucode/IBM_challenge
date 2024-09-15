// theme.ts
import { createTheme } from '@mui/material/styles';

// Define a custom theme
const theme = createTheme({
	palette: {
		primary: {
			main: '#1976d2',
			light: '#020122',
			dark: '#010400',
		},
		secondary: {
			main: '#dc004e',
		},
		text: {
			primary: '#ebebeb',
		},
	},
});



export default theme;
