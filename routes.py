from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from models import File, Classroom
from database import get_db
import io

router = APIRouter()

@router.post("/classroom/{classroom_id}/upload/")
def upload_file(
    classroom_id: int, 
    file: UploadFile = File(...), 
    user_id: int = Depends(get_current_user),  # Ensure user is logged in
    db: Session = Depends(get_db)
):
    classroom = db.query(Classroom).filter(Classroom.id == classroom_id).first()
    
    if not classroom:
        raise HTTPException(status_code=404, detail="Classroom not found")

    if classroom.created_by != user_id:
        raise HTTPException(status_code=403, detail="You are not the owner of this classroom")

    file_data = file.file.read()
    new_file = File(
        # filename=file.filename,
        file_data=file_data,
        uploaded_by=user_id,
        classroom_id=classroom_id
    )

    db.add(new_file)
    db.commit()
    db.refresh(new_file)

    return {"message": "File uploaded successfully"}

@router.get("/classroom/{classroom_id}/files/")
def get_files(classroom_id: int, db: Session = Depends(get_db)):
    files = db.query(File).filter(File.classroom_id == classroom_id).all()
    return [{"id": file.id, "filename": file.filename, "uploaded_by": file.uploaded_by} for file in files]

from fastapi.responses import StreamingResponse

@router.get("/files/{file_id}/download/")
def download_file(file_id: int, db: Session = Depends(get_db)):
    file = db.query(File).filter(File.id == file_id).first()

    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    return StreamingResponse(io.BytesIO(file.file_data), media_type="application/octet-stream", 
                             headers={"Content-Disposition": f"attachment; filename={file.filename}"})
