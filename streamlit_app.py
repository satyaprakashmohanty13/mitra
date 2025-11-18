import streamlit as st
from mitra import process_files
import os

st.title("Mitra - File Transformation Tool")

uploaded_file1 = st.file_uploader("Choose the first file")
uploaded_file2 = st.file_uploader("Choose the second file")

transformation_type = st.radio(
    "Select the transformation type",
    ('Stack', 'Parasite', 'Zipper', 'Cavity', 'Overlap')
)

if st.button('Generate'):
    if uploaded_file1 is not None and uploaded_file2 is not None:
        try:
            fdata1 = uploaded_file1.getvalue()
            fdata2 = uploaded_file2.getvalue()

            generated_data = process_files(fdata1, fdata2, transformation_type)

            if generated_data:
                st.download_button(
                    label="Download Generated File",
                    data=generated_data,
                    file_name="generated_file.dat",
                )
            else:
                st.write("File generation failed. Please try again with different files or transformation type.")

        except ValueError as e:
            st.write(e)
    else:
        st.write("Please upload both files to generate a new file.")
