#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
from PyPDF2 import PdfFileWriter, PdfFileReader
from utils import print_err, print_info, print_notice, print_warn


def main(fl, N):

    pdf_reader = PdfFileReader(open(fl, "rb"))

    if N >= pdf_reader.getNumPages():
        print_warn(f"Warnning: page too large. {N} > {pdf_reader.getNumPages()}")
        return 2

    try:
        pdf_writer1 = PdfFileWriter()
        pdf_writer2 = PdfFileWriter()

        for p in range(N):
            pdf_writer1.addPage(pdf_reader.getPage(p))

        for p in range(N, pdf_reader.getNumPages()):
            pdf_writer2.addPage(pdf_reader.getPage(p))

        file1 = f'{fl}'.rstrip('.pdf') + "-part01.pdf"
        with open(file1, "wb") as fp1:
            pdf_writer1.write(fp1)

        print_info(f"Build {file1} done")

        file2 = f'{fl}'.rstrip('.pdf') + "-part02.pdf"
        with open(file2, "wb") as fp2:
            pdf_writer2.write(fp2)

        print_info(f"Build {file2} done")

    except Exception as e:
        print_err(f"Error: {e}")

    else:
        return 0


if __name__ == '__main__':

    if len(sys.argv) != 3:
        print("Usage {} pdffile Npages")
        sys.exit(1)

    fl = sys.argv[1]
    num = sys.argv[2]

    if not num.isnumeric():
        print("Usage {} pdffile Npages")
        sys.exit(1)

    sys.exit(not main(fl, int(num)))
