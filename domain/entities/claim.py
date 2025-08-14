from pydantic import BaseModel, EmailStr
from typing import Optional, Literal
from datetime import date

class Claim(BaseModel):

    #Akun Pemegang Polis
    user_id: int

    # Data Pemegang Polis
    nomor_polis: str
    nama_pemegang: str
    alamat_korespondensi: str
    kota_pemegang: str
    kode_pos_pemegang: str
    telp_rumah: Optional[str]
    telp_kantor: Optional[str]
    telp_hp: Optional[str]
    email: Optional[EmailStr]

    # Data Tertanggung
    nama_tertanggung: str
    tempat_lahir_tertanggung: str
    tanggal_lahir_tertanggung: date
    jenis_kelamin: str
    pekerjaan_tertanggung: str
    nama_perusahaan: Optional[str]
    kota_perusahaan: Optional[str]
    kode_pos_perusahaan: Optional[str]

    # Riwayat Penyakit / Cedera
    tanggal_perawatan: date
    nama_dokter_rumah_sakit: str
    deskripsi_penyakit: str
    berhubungan_kecelakaan: bool
    tanggal_kecelakaan: Optional[date]

    #Claim Tracker
    status: Literal["dikirim", "review", "diterima", "ditolak"] = "dikirim"

    # created_at : str
    # updated_at : str
