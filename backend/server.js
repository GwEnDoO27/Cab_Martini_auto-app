const express = require('express');
const cors = require('cors'); // Import cors
const app = express();

// Import the routes
const routeIndex = require('./routes/index'); // Import the index route file

// Enable CORS for React frontend running on port 3000
app.use(cors({
    origin: 'http://localhost:3000', // Allow requests from your React app
    methods: 'GET,POST', // Allow specific HTTP methods
}));

app.use(express.urlencoded({ extended: true })); // Parse URL-encoded bodies
app.use(express.json()); // Enable JSON parsing for incoming requests

// Use the routes
app.use('/', routeIndex);
console.log('Server is running');

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
