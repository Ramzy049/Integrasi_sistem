from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(
    title="Tugas 1 Integrasi Sistem",
    description="Tugas 1 Integrasi Sistem",
    version="1.0.0"
)

# Model data (dipakai untuk POST: semua field wajib diisi)
class Mahasiswa(BaseModel):
    nama: str
    alamat: str
    ipk: float
    semester: int
    hobi: str

# Model untuk PUT: semua field opsional, jadi boleh ubah sebagian saja
class MahasiswaUpdate(BaseModel):
    nama: Optional[str] = None
    alamat: Optional[str] = None
    ipk: Optional[float] = None
    semester: Optional[int] = None
    hobi: Optional[str] = None

# Simulasi database (hilang kalau server mati/reload)
mahasiswa_db = {}

# ROOT
@app.get("/")
def read_root():
    return {"message": "API Data Mahasiswa"}

# READ ALL (GET)
@app.get("/mahasiswa")
async def read_all_mahasiswa():
    return mahasiswa_db

# CREATE (POST)
@app.post("/mahasiswa/{mahasiswa_id}")
async def create_mahasiswa(mahasiswa_id: int, mahasiswa: Mahasiswa):
    if mahasiswa_id in mahasiswa_db:
        raise HTTPException(status_code=409, detail="Mahasiswa sudah ada")
    mahasiswa_db[mahasiswa_id] = mahasiswa.model_dump()
    return {"message": "Mahasiswa berhasil ditambahkan", "mahasiswa": mahasiswa_db[mahasiswa_id]}

# READ (GET)
@app.get("/mahasiswa/{mahasiswa_id}")
async def read_mahasiswa(mahasiswa_id: int):
    if mahasiswa_id not in mahasiswa_db:
        raise HTTPException(status_code=404, detail="Mahasiswa tidak ditemukan")
    return {"mahasiswa_id": mahasiswa_id, "mahasiswa": mahasiswa_db[mahasiswa_id]}

# UPDATE (PUT)
@app.put("/mahasiswa/{mahasiswa_id}")
async def update_mahasiswa(mahasiswa_id: int, mahasiswa: MahasiswaUpdate):
    if mahasiswa_id not in mahasiswa_db:
        raise HTTPException(status_code=404, detail="Mahasiswa tidak ditemukan")
    mahasiswa_db[mahasiswa_id].update(mahasiswa.model_dump(exclude_unset=True))
    return {"message": "Mahasiswa berhasil diubah", "mahasiswa": mahasiswa_db[mahasiswa_id]}

# DELETE (DELETE)
@app.delete("/mahasiswa/{mahasiswa_id}")
async def delete_mahasiswa(mahasiswa_id: int):
    if mahasiswa_id not in mahasiswa_db:
        raise HTTPException(status_code=404, detail="Mahasiswa tidak ditemukan")
    deleted = mahasiswa_db.pop(mahasiswa_id)
    return {"message": "Mahasiswa berhasil dihapus", "mahasiswa": deleted}