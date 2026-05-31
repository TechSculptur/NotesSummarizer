from fastapi import FastAPI,UploadFile,File,HTTPException
from fastapi.responses import HTMLResponse,FileResponse
import shutil
import os
from preprocessing import extract,generator,summarizer    
os.makedirs("uploads", exist_ok=True)
os.makedirs("summary", exist_ok=True)
app=FastAPI()
MAX_SIZE = 100* 1024 * 1024 
@app.get("/")
def home():
    return HTMLResponse("""
    <html>
        <body>
            <h2>Upload PDF</h2>
            <form action="/upload" enctype="multipart/form-data" method="post">
                <input type="file" name="file">
                <input type="submit">
            </form>
        </body>
    </html>
    """)
@app.post('/upload')
async def upload(file:UploadFile=File(...)):
    content=await file.read()
    if(len(content)>MAX_SIZE):
        raise HTTPException(status_code=404,detail='file size too big')
    if(file.content_type!='application/pdf'):
        raise HTTPException(status_code=404,detail='invalid file type only PDFs supported')
    file_path=f"uploads/{file.filename}"
    with open(file_path, "wb") as buffer:
        buffer.write(content)
    text=extract.extract_text()
    summary=summarizer.generate_summary(text)
    path=os.path.join('summary',f'summary_{file.filename}')
    generator.generate_pdf(summary,path)
    return FileResponse(
    path=path,
    media_type='application/pdf',
    filename=f'summary_{file.filename}')
