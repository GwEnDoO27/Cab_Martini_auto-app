const express = require('express');
const router = express.Router();

const ediToXlsxRoute = require('./ediToXlsxRoute');
// const pdfToXmlRoute = require('./pdfToXmlRoute');

router.use('/edi_to_xlsx', ediToXlsxRoute);
// router.use('/pdf_to_xml', pdfToXmlRoute);

module.exports = router;
