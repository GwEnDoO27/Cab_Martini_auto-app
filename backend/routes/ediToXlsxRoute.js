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
router.post('/upload-file', upload.array('files'), (req, res) => {
    console.log(req.files)

    if (!req.files || req.files.length === 0) {
        return res.status(400).send('Aucun fichier téléchargé.');
    }

    lastUploadedFile = req.files.map(file => file.originalname); // Store the filename in the variable
    console.log("lastUploadedFile", lastUploadedFile)

    // Send back a success message and the name of the uploaded file
    res.send({
        message: `Le(s) fichier(s) suivant(s) a/ont bien été téléchargé(s) : ${lastUploadedFile.join(', ')}`,
        fileName: lastUploadedFile, // Send back the name of the uploaded file
    });
});


// Define the route to run the Python script for formatting
router.get('/formatting', async (req, res) => {
    if (!lastUploadedFile || lastUploadedFile.length === 0) {
        return res.status(400).send('Aucun fichier n\'a été téléchargé.');
    }

    try {
        const outputs = [];
        const files = Array.isArray(lastUploadedFile) ? lastUploadedFile : [lastUploadedFile];

        for (const element of files) {
            const filePath = `./uploads/${element}`;
            const output = await runPythonScript(`python-scripts/extracting_xlsx.py ${filePath}`);
            outputs.push({ filename: element, output });
        }

        res.json(outputs);
    } catch (error) {
        console.error(error);
        res.status(500).send(error.toString());
    }
});

const zip = require('express-zip');
const path = require('path');
const fs = require('fs');

// Serve the converted Excel files
router.get('/download', (req, res) => {
    if (!lastUploadedFile || lastUploadedFile.length === 0) {
        return res.status(400).send('Aucun fichier n\'a été téléchargé.');
    }

    const files = Array.isArray(lastUploadedFile) ? lastUploadedFile : [lastUploadedFile];
    console.log("files", files) 
    
    const zipFiles = files.map(file => ({
        path: path.join('./downloads', `${file.replace('.txt','.xlsx')}`),
        name: `${file.replace('.txt','.xlsx')}`,
    }));

    console.log("zipFiles", zipFiles)

    //const existingFiles = zipFiles.filter(file => fs.existsSync(file.path));

    //console.log("existingFiles", existingFiles)

    if (zipFiles.length === 0) {
        return res.status(404).send('Aucun fichier .xlsx trouvé.');
    }


    res.zip(zipFiles, 'excel_files.zip', (err) => {
        if (err) {
            console.error('Zip error:', err);
            return res.status(500).send('Erreur lors de la création du fichier zip.');
        }
        res.end(); // Explicitly end the response
    });
});

module.exports = router;