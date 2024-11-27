import React from 'react';
import { Route, BrowserRouter as Router, Routes } from 'react-router-dom';
import EdiToXlsxPage from './components/EdiToXlsxPage'; // Import the EdiToXlsxPage component
import HomePage from './components/HomePage'; // Import the HomePage component
import PdfToXmlPage from './components/PdfToXmlPage'; // Import the PdfToXmlPage component

const App = () => {
    return (
        <Router>
            <div>
                <Routes>
                    {/* Defining routes here using the new 'Routes' component */}

                    {/* Home page route */}
                    <Route exact path="/" element={<HomePage />} />

                    {/* Formatting EDI to XLSX route */}
                    <Route path="/edi_to_xlsx" element={<EdiToXlsxPage />} />

                    {/* Formatting PDF to XML route */}
                    <Route path="/pdf_to_xml" element={<PdfToXmlPage />} />

                </Routes>
            </div>
        </Router>
    );
};

export default App;
