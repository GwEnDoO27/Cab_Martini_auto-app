import React from 'react';
import { useNavigate } from 'react-router-dom'; // Import useNavigate
import '../style.css'; // Import the CSS module

const HomePage = () => {
    const navigate = useNavigate(); // Call useNavigate to get the navigate function

    const handleEdiXlsxClick = () => {
        navigate('/edi_to_xlsx'); // Navigate to the '/edi_to_xlsx' route
    };

    const handlePdfXmlClick = () => {
        navigate('/pdf_to_xml'); // Navigate to the '/pdf_to_xml' route
    };

    return (
        <>
            <header>
                <h1>Répertoire des applications</h1>
            </header>
            <div class='btns-container'>
                <button onClick={handleEdiXlsxClick}>Convertir fichier EDI (.txt) en fichier Excel</button>
            </div>
            <button onClick={handlePdfXmlClick}>Convertir fichier PDF en XML</button>
            {/* <div className={styles.container}>
            </div> */}
        </>
    );
};

export default HomePage;
