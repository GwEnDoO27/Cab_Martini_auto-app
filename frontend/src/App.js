import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import HomePage from './components/HomePage'; // Import the HomePage component
import EdiToCsvPage from './components/EdiToCsvPage'; // Import the EdiToCsvPage component
import PdfToXmlPage from './components/PdfToXmlPage'; // Import the PdfToXmlPage component

const App = () => {
    return (
        <Router>
            <div>
                <Routes>
                    {/* Defining routes here using the new 'Routes' component */}

                    {/* Home page route */}
                    <Route exact path="/" element={<HomePage/>} />

                    {/* Formatting EDI to CSV route */}
                    <Route path="/edi_to_csv" element={<EdiToCsvPage/>} />

                    {/* Formatting PDF to XML route */}
                    <Route path="/pdf_to_xml" element={<PdfToXmlPage/>} />

                </Routes>
            </div>
        </Router>
    );
};

export default App;
