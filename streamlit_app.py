import streamlit as st
from mitra import process_files
import os

# Updated application name
st.title("Polyglot File Generator")

uploaded_file1 = st.file_uploader("Choose the FIRST (Host) file")
uploaded_file2 = st.file_uploader("Choose the SECOND (Payload) file")

# Added the mandatory note about file format roles
st.markdown("""
<div style="background-color: #ffeaea; padding: 10px; border-radius: 8px; border: 1px solid #ff0000; margin-bottom: 20px;">
    <strong>⚠️ Important Note on File Order</strong>
    <p style="margin-top: 5px; font-size: 0.9em;">
    The FIRST file you upload <strong>MUST</strong> be a format capable of acting as a "Host" for the payload.
    </p>
    <p style="margin-top: 5px; font-size: 0.9em;">
    <strong>❌ Never choose these formats as the SECOND (Payload) file:</strong> They rely on strict footers or structures that break when modified, preventing them from being hosted inside other formats.
    </p>
    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-top: 10px; font-size: 0.85em;">
        <div>
            <strong>Image formats:</strong> PNG, JPG/JPEG, GIF, TIFF, ICO, PSD, BPG
        </div>
        <div>
            <strong>Executable / System:</strong> ELF, PE (EXE/DLL), LNK, NES, Java (class), WASM
        </div>
        <div>
            <strong>Archive / Compressed:</strong> BZ2, GZ, CAB, CPIO
        </div>
        <div>
            <strong>Media formats:</strong> MP4, FLAC, OGG, ID3v2, ILDA
        </div>
        <div>
            <strong>Document formats:</strong> RTF, AR, PostScript (PS)
        </div>
        <div>
            <strong>Misc Binary:</strong> BMP, EBML (MKV, WebM), ICC, WAD, PCAP, PCAPNG, ID3v1, XZ
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


transformation_type = st.radio(
    "Select the transformation type",
    ('Stack', 'Parasite', 'Zipper', 'Cavity', 'Overlap')
)

if st.button('Generate'):
    if uploaded_file1 is not None and uploaded_file2 is not None:
        try:
            fdata1 = uploaded_file1.getvalue()
            fdata2 = uploaded_file2.getvalue()

            # Note: The 'process_files' function is assumed to be defined in 'mitra.py'
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

