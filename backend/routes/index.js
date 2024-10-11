const express = require('express');
const router = express.Router();

const ediToCsvRoute = require('./ediToCsvRoute');
const pdfToXmlRoute = require('./pdfToXmlRoute');

router.use('/edi_to_csv', ediToCsvRoute);
// router.use('/pdf_to_xml', pdfToXmlRoute);

module.exports = router;
