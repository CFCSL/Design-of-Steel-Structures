import streamlit as st
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
import math
import os,re
import base64
from io import BytesIO

# Define a function to create a download link
def download_link(df, file_name, file_label='Download Excel file'):
    """
    Generates a link to download the given pandas DataFrame as an Excel file.

    Parameters:
    - df: pandas DataFrame
    - file_name: str, the name of the downloaded file (without the extension)
    - file_label: str, the label of the download link

    Returns:
    - str, the HTML code for the download link
    """
    # Create a BytesIO object to write the Excel file to
    excel_buffer = BytesIO()
    with pd.ExcelWriter(excel_buffer) as writer:
        df.to_excel(writer, index=False)
    # Convert the Excel file in the BytesIO object to a base64 string
    b64 = base64.b64encode(excel_buffer.getvalue()).decode()
    # Create the download link
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{file_name}.xlsx">{file_label}</a>'
    return href


collect_numbers = lambda x : [float(i) for i in re.findall(r"[-+]?(?:\d*\.\d+|\d+)", x)  if i != "" ]
