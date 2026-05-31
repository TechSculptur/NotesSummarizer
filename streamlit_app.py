import streamlit as st
import requests

st.set_page_config(page_title="AI Notes Analyzer")

st.title("📄 AI Notes Analyzer")
st.write("Upload a PDF and get a summarized PDF.")

uploaded_file = st.file_uploader(
    "Choose a PDF",
    type=["pdf"]
)

if uploaded_file is not None:

    if st.button("Generate Summary"):

        with st.spinner("Generating summary..."):

            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file,
                    "application/pdf"
                )
            }

            response = requests.post(
                    "https://notessummarizer-7zi7.onrender.com/upload",
                    files=files
            )

            if response.status_code == 200:

                st.success("Summary generated!")

                st.download_button(
                    label="📥 Download Summary PDF",
                    data=response.content,
                    file_name=f"summary_{uploaded_file.name}",
                    mime="application/pdf"
                )

            else:

                st.error(
                    f"Error: {response.status_code}"
                )

                try:
                    st.write(response.json())
                except:
                    st.write(response.text)
