import React, { useState } from 'react';

const EdiToCsvPage = () => {
    const [selectedFile, setSelectedFile] = useState(null);
    const [output, setOutput] = useState(''); // For storing the output
    const [errorMessage, setErrorMessage] = useState(''); // For storing the error message

    const handleFileChange = (event) => {
        setSelectedFile(event.target.files[0]); // Save the selected file
    };

    const uploadFile = async () => {
        if (!selectedFile) {
            alert('Veuillez sélectionner un fichier.');
            return;
        }

        const formData = new FormData();
        formData.append('file', selectedFile); // Append the file to the FormData

        try {
            const response = await fetch('http://localhost:5000/edi_to_csv/upload-file', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json(); // Parse JSON response
            alert(data.message); // Show success message

        } catch (error) {
            console.error('Error uploading file:', error);
            alert('Error uploading file');
        }
    };

    // const runScript = () => {
    //     setOutput(''); // Clear previous output
    //     setErrorMessage(''); // Clear previous error message

    //     fetch('/edi_to_csv/formatting')
    //         .then(response => {
    //             if (!response.ok) {
    //                 throw new Error('Network response was not ok');
    //             }

    //             const contentType = response.headers.get('content-type');
    //             if (contentType && contentType.indexOf('application/json') !== -1) {
    //                 return response.json();  // Parse JSON if content type is correct
    //             } else {
    //                 throw new Error('Received non-JSON response');
    //             }
    //         })
    //         .then(data => {
    //             // Now process the data
    //             if (data.success) {
    //                 setOutput(data.stdout);
    //                 setErrorMessage(data.stderr || '');
    //             } else {
    //                 setErrorMessage(data.message + (data.stderr ? `\n${data.stderr}` : ''));
    //             }
    //         })
    //         .catch(err => {
    //             // Handle errors, e.g., JSON parsing errors or network issues
    //             setErrorMessage(`An error occurred: ${err.message}`);
    //         });
    // };

    return (
        <div id="box">

            <div id="header">
                <h3>Homepage</h3>
            </div>

            <div id="convert">
                <h1>Convertir fichier EDI en CSV</h1>
                <input type="file" onChange={handleFileChange} />
                <div id="error-message">{errorMessage}</div>
                {/* <button id="run-formatting-btn" onClick={runScript}>Formatter le fichier en CSV</button> */}
                <button onClick={uploadFile}>Envoyer le fichier</button>
            </div>

            <div id="result">
            <h3>Aperçu : </h3>
            <pre id="output">{output}</pre>
            </div>

        </div>
    );
};

export default EdiToCsvPage;
