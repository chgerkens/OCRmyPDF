#! /usr/bin/env python
import sys
import glob
import os
import shutil
import argparse
import logging
from string import Template
logging.basicConfig(level=logging.INFO)
ocrCommandTemplate = Template('OCRmyPDF.sh "$inputPdfFile" "$outputPdfFile"')

parser = argparse.ArgumentParser(description='OCR processing of multiple PDF files')
parser.add_argument('-input', nargs=1, required=True, help='Directory of PDF files to process')
parser.add_argument('-output', nargs=1, required=True, help='Directory of successful processed OCR PDF files')
parser.add_argument('-original', nargs=1, required=True, help='Directory for backup of original PDF files')
parser.add_argument('-error', nargs=1, required=True, help='Directory for storing PDF files that could not be processed for certain reasons')

args = parser.parse_args()
inputDir = args.input[0]
outputDir = args.output[0]
originalDir = args.original[0]
errorDir = args.error[0]

logging.info('Input directory: ' + inputDir)
logging.info('Output directory: ' + outputDir)
logging.info('Original backup directory: ' + originalDir)
logging.info('Error directory: ' + errorDir)

inputPdfs = glob.glob(inputDir+'/*.pdf')

logging.info('PDF files to process:')
print(inputPdfs)
for inputPdf in inputPdfs:
    logging.info('Start processing ' + inputPdf)
    outputPdf = outputDir + os.path.sep + os.path.basename(inputPdf)
    logging.debug('Output is written to ' + outputPdf)
    resultCode = os.system(ocrCommandTemplate.substitute(inputPdfFile=inputPdf, outputPdfFile=outputPdf))
    if resultCode == 0 and os.path.isfile(outputPdf):
        logging.info(inputPdf + ' processing finished.')
        shutil.move(inputPdf, originalDir)
    else:
        logging.error(inputPdf + ' processing failed.')
        shutil.move(inputPdf, errorDir)