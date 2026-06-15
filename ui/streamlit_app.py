import streamlit as st
import requests

st.set_page_config(page_title="ContraDoc AI", page_icon="⚡", layout="wide")

st.title("⚡ ContraDoc AI")
st.subheader("Find contradictions across multiple documents")
st.write("---")

st.header("📂 Step 1: Upload Your Documents")
uploaded_files = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        try:
            res = requests.post(
                "http://127.0.0.1:8000/upload",
                files={"file": (file.name, file, "application/pdf")}
            )
            st.success(f"✅ {file.name} uploaded!")
        except Exception as e:
            st.error(f"❌ Upload failed: {e}")
if st.button("⚙️ Build Knowledge Base", use_container_width=True):
    with st.spinner("Building..."):
        res = requests.post("http://127.0.0.1:8000/build")
        st.success("✅ Knowledge base built with all documents!")
st.write("---")
st.header("🔍 Step 2: Ask a Question")
query = st.text_input("What topic?", placeholder="e.g. What causes climate change?")

if st.button("🔍 Find Contradictions", use_container_width=True):
    if query:
        with st.spinner("Analyzing... please wait 15-20 seconds"):
            try:
                res = requests.post(
                    "http://127.0.0.1:8000/analyze",
                    json={"question": query},
                    timeout=60
                )
                result = res.json()
                st.write("---")
                st.header("RESULTS")
                st.write("**Sources:**", result.get("sources_used", []))
                analysis = result.get("analysis", "No analysis returned")
                if "Yes" in str(analysis):
                    st.error("⚠️ CONTRADICTION DETECTED!")
                else:
                    st.success("✅ No contradiction found")
                st.markdown("### Analysis")
                st.write(analysis)
            except Exception as e:
                st.error(f"❌ Error: {e}")
    else:
        st.warning("Please enter a question!")