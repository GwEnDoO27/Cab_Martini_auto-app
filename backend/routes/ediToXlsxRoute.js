const express = require('express');
const router = express.Router();
const multer = require('multer');
const path = require('path');

const { runPythonScript } = require('../helpers/runPython');

// Set up multer for file upload
const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, 'uploads/'); // Folder where files will be saved
    },
    filename: (req, file, cb) => {
        cb(null, file.originalname); // Keep the original file name
    },
});

const upload = multer({ storage });
let lastUploadedFile = ''; // Variable to store the last uploaded file name

// Upload file route
router.post('/upload-file', upload.single('file'), (req, res) => {

    if (!req.file) {
        return res.status(400).send('Aucun fichier téléchargé.');
    }

    lastUploadedFile = req.file.originalname; // Store the filename in the variable

    // Send back a success message and the name of the uploaded file
    res.send({
        message: `Le fichier suivant a bien été téléchargé : ${req.file.originalname}`,
        fileName: req.file.originalname, // Send back the name of the uploaded file
    });
});


// Define the route to run the Python script for formatting
router.get('/formatting', async (req, res) => {
    if (!lastUploadedFile) {
        return res.status(400).send('Aucun fichier n\'a été téléchargé.');
    }

    try {
        // Send the output back to the client
        const filePath = `./uploads/${lastUploadedFile}`;
        const output = await runPythonScript(`python-scripts/extracting_xlsx.py ${filePath}`);
        res.send(output);
    } catch (error) {
        res.status(500).send(error.message);
    }
});

// Serve the Excel file
router.get('/download', (req, res) => {
    const filePath = "../downloads/excel_values.xlsx"

    res.download(filePath, (err) => {
        if (err) {
            console.error(err);
            res.status(404).send('File not found');
        }
    });
});

module.exports = router;