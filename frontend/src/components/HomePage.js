import React from 'react';
import styles from './App.module.css'; // Import the CSS module
import { useNavigate } from 'react-router-dom'; // Import useNavigate

const HomePage = () => {
    const navigate = useNavigate(); // Call useNavigate to get the navigate function

    const handleEdiCsvClick = () => {
        navigate('/edi_to_csv'); // Navigate to the '/edi_to_csv' route
    };

    const handlePdfXmlClick = () => {
        navigate('/pdf_to_xml'); // Navigate to the '/pdf_to_xml' route
    };

    return (
        <>
            <div className={styles.header}>
                <h1>Répertoire Applications</h1>
            </div>
            <div className={styles.container}>
                <button className={styles.button} onClick={handleEdiCsvClick}>Convertir fichier EDI en CSV</button>
            </div>
            <div className={styles.container}>
                <button className={styles.button} onClick={handlePdfXmlClick}>Convertir fichier PDF en XML</button>
            </div>
        </>
    );
};

export default HomePage;
