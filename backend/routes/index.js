const express = require('express');
const router = express.Router();

const ediToXlsxRoute = require('./ediToXlsxRoute');
// const pdfToXlsxRoute = require('./pdfToXlsxRoute');

router.use('/edi_to_xlsx', ediToXlsxRoute);
// router.use('/pdf_to_xlsx', pdfToXlsxRoute);

module.exports = router;
