"""
Extract crime data from NCRB PDF reports and convert to CSV format.
Requires: pip install PyPDF2 tabula-py pandas
"""

import pandas as pd
import os
import sys

def extract_ncrb_pdf_manual():
    """
    Guide for manually extracting data from NCRB PDF.
    """
    print("="*70)
    print("NCRB PDF DATA EXTRACTION GUIDE")
    print("="*70)
    
    print("\nThe NCRB PDF you found is a comprehensive report.")
    print("Here's how to extract usable data:\n")
    
    print("METHOD 1: Use Online PDF to CSV Converter")
    print("-" * 70)
    print("1. Download the PDF:")
    print("   https://ncrb.gov.in/uploads/n