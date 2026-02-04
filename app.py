import streamlit as st
from fastapi import FastAPI, File, UploadFile, HTTPException
import uvicorn
import os
import shutil
from datetime import datetime

# Create uploads directory
UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# Initialize FastAPI app
app = FastAPI(title="Video Upload API")

@app.post("/api/upload")
async def upload_video(file: UploadFile = File(...)):
    try:
        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{file.filename}"
        file_path = os.path.join(UPLOAD_DIR, filename)
        
        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        return {
            "status": "success",
            "message": "File uploaded successfully",
            "filename": filename,
            "file_size": os.path.getsize(file_path),
            "upload_time": timestamp
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/files")
async def list_files():
    files = []
    if os.path.exists(UPLOAD_DIR):
        for file in os.listdir(UPLOAD_DIR):
            file_path = os.path.join(UPLOAD_DIR, file)
            if os.path.isfile(file_path):
                files.append({
                    "name": file,
                    "size": os.path.getsize(file_path),
                    "modified": datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat()
                })
    return {"files": files}

# Streamlit interface
def main():
    st.title("🎥 Video Upload Server")
    st.markdown("---")
    
    # Display server status
    st.success("✅ Server is running and ready to receive uploads!")
    
    # Show upload instructions
    st.subheader("Upload Instructions")
    st.markdown("""
    Use the Tkinter client to upload videos to this server.
    
    **API Endpoints:**
    - `POST /api/upload` - Upload video file
    - `GET /api/files` - List uploaded files
    """)
    
    # Show uploaded files
    st.subheader("Uploaded Files")
    if os.path.exists(UPLOAD_DIR):
        files = os.listdir(UPLOAD_DIR)
        if files:
            for file in files:
                file_path = os.path.join(UPLOAD_DIR, file)
                file_size = os.path.getsize(file_path)
                modified_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                
                col1, col2, col3 = st.columns([3, 2, 2])
                col1.write(file)
                col2.write(f"{file_size/1024/1024:.2f} MB")
                col3.write(modified_time.strftime("%Y-%m-%d %H:%M"))
        else:
            st.info("No files uploaded yet")
    else:
        st.info("Upload directory not found")

if __name__ == "__main__":
    # Run both Streamlit and FastAPI
    import threading
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "api":
        # Run only API server
        uvicorn.run(app, host="0.0.0.0", port=8000)
    else:
        # Run Streamlit app
        main()
