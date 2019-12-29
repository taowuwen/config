#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
from PyPDF2 import PdfFileWriter, PdfFileReader
from utils import print_err, print_info, print_notice

def pdfmerge(output, filelist):
    pdf_writer = PdfFileWriter()

    for fl in filelist:
        try:
            pdf_reader = PdfFileReader(fl)
            print_notice(f"handle file: {os.path.basename(fl)}...")
            for page in range(pdf_reader.getNumPages()):
                pdf_writer.addPage(pdf_reader.getPage(page))
        except FileNotFoundError as e:
            print_err(f"Error: File Not Found {fl}")
            return 1

    try:
        with open(output, 'wb') as fp:
            print_notice(f"Writting file: {os.path.basename(output)}...")
            pdf_writer.write(fp)
    except Exception as e:
        print_err(f"{e}")
    else:
        print_info(f"Success build file {output}.")


def main(filelist=[], output=None):
    output = os.path.realpath(os.path.expanduser(output))

    return pdfmerge(output, [os.path.realpath(os.path.expanduser(fl)) for fl in filelist])

if __name__ == '__main__':

    if len(sys.argv) < 3:
        print("Usage {} pdffile [...] output")
        sys.exit(1)

    sys.exit(not main(sys.argv[1:-1], sys.argv[-1]))
