import React, { useState } from 'react';

const EdiToXlsxPage = () => {
    const [selectedFile, setSelectedFile] = useState(null);
    const [output] = useState(''); // For storing the output
    const [errorMessage] = useState(''); // For storing the error message

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
        console.log('Fichier a envoyer:', selectedFile);
        try {
            const response = await fetch('http://localhost:4000/edi_to_xlsx/upload-file', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                console.log(response)
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json(); // Parse JSON response
            alert(data.message); // Show success message

        } catch (error) {
            console.error('Error uploading file:', error);
            alert('Error uploading file');
        }
    };


    const format = async () => {
        try {
            const response = await fetch('http://localhost:4000/edi_to_xlsx/formatting', {
                method: 'GET', // Change to GET for triggering the script
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            alert("Le fichier a bien été formatté.");
        } catch (error) {
            console.error('Error running script:', error);
            alert('Le fichier a déjà été formatté ou aucun fichier n\'a été envoyé.');
        }
    };

    const handleDownload = () => {
        const fileUrl = 'http://localhost:4000/edi_to_xlsx/download';
        const link = document.createElement('a');
        link.href = fileUrl;
        link.download = ''; // This will download the file with its original name
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    };

    return (
        <div id="box">
            <header>
                <h1>Répertoire des applications</h1>
            </header>
            <div class="convert-btn">
                <h2>Convertir fichier EDI (.txt) en fichier Excel</h2>
                <p>Choisissez un fichier EDI à convertir en fichier Excel.</p>
            </div>

            <div id="convert">
                <input type="file" onChange={handleFileChange} name='file'/>
                <div id="error-message">{errorMessage}</div>
                <p>Le fichier sélectionné est : {selectedFile ? selectedFile.name : 'Aucun fichier sélectionné'}</p>
                <p>Appuyez sur le bouton ci-dessous pour envoyer le fichier. Puis, formattez le :</p>
                <button onClick={uploadFile}>Récupérer le fichier</button>
                <button class="formatting-btn" onClick={format}>Formatter le fichier en Excel.</button>
            </div>

            <div class="result">
                <pre id="output">{output}</pre>
                <p>Téléchargez le fichier ci-dessous :</p>

                <button onClick={handleDownload}>Télécharger le fichier</button>

            </div>
        </div>
    );
};

export default EdiToXlsxPage;
