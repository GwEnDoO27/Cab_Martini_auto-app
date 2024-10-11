const express = require('express');
const router = express.Router();
const multer = require('multer');

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
        const filePath = `./uploads/${lastUploadedFile}`;
        const output = await runPythonScript(`python-scripts/extracting_csv.py ${filePath}`);

        // Send both stdout and stderr in the response
        res.json({
            success: true,
            stdout: output.stdout,
            stderr: output.stderr || null // Send stderr if present
        });
    } catch (error) {
        // If an error occurs, send both the error message and stderr
        res.status(500).json({
            success: false,
            message: `Une erreur est survenue : ${error.message}`,
            stderr: error.stderr || null
        });
    }
});

module.exports = router;