import streamlit as st
import os
from datetime import datetime
import shutil
from io import BytesIO

# Konfigurasi halaman
st.set_page_config(
    page_title="Video Uploader",
    page_icon="🎥",
    layout="wide"
)

# Create uploads directory
UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# Header
st.title("🎥 Video Uploader")
st.markdown("---")

# Tabs untuk navigasi
tab1, tab2 = st.tabs(["📤 Upload", "📁 Uploaded Files"])

with tab1:
    st.subheader("Upload Video File")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose a video file to upload",
        type=["mp4", "avi", "mov", "mkv", "webm", "wmv"],
        accept_multiple_files=False,
        key="video_uploader"
    )
    
    if uploaded_file is not None:
        # Display file information
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Filename", uploaded_file.name)
        with col2:
            st.metric("Size", f"{uploaded_file.size / (1024*1024):.2f} MB")
        with col3:
            st.metric("Type", uploaded_file.type)
        
        # Preview video
        st.subheader("Preview")
        st.video(uploaded_file)
        
        # Upload options
        st.subheader("Save Options")
        custom_filename = st.text_input("Custom filename (optional)", value=uploaded_file.name)
        
        # Save button
        if st.button("💾 Save Video", type="primary", use_container_width=True):
            try:
                with st.spinner("Saving video..."):
                    # Generate filename
                    if custom_filename != uploaded_file.name:
                        filename = custom_filename
                    else:
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = f"{timestamp}_{uploaded_file.name}"
                    
                    file_path = os.path.join(UPLOAD_DIR, filename)
                    
                    # Save file
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    st.success(f"✅ Video saved successfully as: **{filename}**")
                    st.info(f"File size: {os.path.getsize(file_path) / (1024*1024):.2f} MB")
                    
                    # Show download button
                    with open(file_path, "rb") as file:
                        st.download_button(
                            label="📥 Download Saved Video",
                            data=file,
                            file_name=filename,
                            mime=uploaded_file.type,
                            use_container_width=True
                        )
                        
            except Exception as e:
                st.error(f"❌ Error saving file: {str(e)}")

with tab2:
    st.subheader("Uploaded Videos")
    
    # Refresh button
    if st.button("🔄 Refresh File List"):
        st.experimental_rerun()
    
    # List uploaded files
    if os.path.exists(UPLOAD_DIR):
        files = sorted([f for f in os.listdir(UPLOAD_DIR) if os.path.isfile(os.path.join(UPLOAD_DIR, f))], 
                      reverse=True)
        
        if files:
            st.markdown(f"Found **{len(files)}** uploaded files")
            
            # Display files in a table-like format
            for i, filename in enumerate(files):
                file_path = os.path.join(UPLOAD_DIR, filename)
                file_size = os.path.getsize(file_path)
                modified_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                
                with st.expander(f"📹 {filename}", expanded=False):
                    col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
                    
                    with col1:
                        st.write("**Size:**")
                        st.write(f"{file_size / (1024*1024):.2f} MB")
                    
                    with col2:
                        st.write("**Modified:**")
                        st.write(modified_time.strftime("%Y-%m-%d %H:%M"))
                    
                    with col3:
                        st.write("**Actions:**")
                        # Read file for download
                        with open(file_path, "rb") as file:
                            st.download_button(
                                label="📥 Download",
                                data=file,
                                file_name=filename,
                                mime="video/mp4",
                                key=f"download_{i}"
                            )
                    
                    with col4:
                        if st.button("🗑️ Delete", key=f"delete_{i}"):
                            try:
                                os.remove(file_path)
                                st.success("File deleted!")
                                st.experimental_rerun()
                            except Exception as e:
                                st.error(f"Error deleting file: {str(e)}")
                    
                    # Try to show preview if it's a video
                    try:
                        if filename.lower().endswith(('.mp4', '.mov', '.avi', '.mkv', '.webm')):
                            with open(file_path, "rb") as video_file:
                                st.video(video_file.read())
                    except:
                        st.info("Preview not available for this file type")
        else:
            st.info("📭 No files uploaded yet. Go to the Upload tab to get started!")
    else:
        st.info("📭 Upload directory not found. Upload your first video!")

# Sidebar dengan informasi
with st.sidebar:
    st.header("ℹ️ About")
    st.markdown("""
    This is a simple video uploader application built with Streamlit.
    
    **Features:**
    - Upload video files (MP4, AVI, MOV, etc.)
    - Preview videos before saving
    - Download saved videos
    - Manage uploaded files
    
    **Storage Location:**
    Files are stored in the `uploads` directory on the server.
    """)
    
    st.divider()
    
    st.markdown("**📊 Storage Info**")
    if os.path.exists(UPLOAD_DIR):
        total_size = sum(os.path.getsize(os.path.join(UPLOAD_DIR, f)) 
                        for f in os.listdir(UPLOAD_DIR) 
                        if os.path.isfile(os.path.join(UPLOAD_DIR, f)))
        file_count = len([f for f in os.listdir(UPLOAD_DIR) 
                         if os.path.isfile(os.path.join(UPLOAD_DIR, f))])
        
        st.metric("Files Stored", file_count)
        st.metric("Total Size", f"{total_size / (1024*1024):.2f} MB")
    else:
        st.metric("Files Stored", "0")
        st.metric("Total Size", "0 MB")

# Footer
st.markdown("---")
st.caption("Built with ❤️ using Streamlit | Video Uploader App")
