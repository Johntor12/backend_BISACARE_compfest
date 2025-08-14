from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from infrastructure.db.connection import Base
import enum

class ClaimStatusEnum(str, enum.Enum):
    dikirim = "dikirim"
    review = "review"
    diterima = "diterima"
    ditolak = "ditolak"


class ClaimModel(Base):
    __tablename__ = "claims"

    id = Column(Integer, primary_key=True, index=True)


    # Relasi ke User
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("UserModel", back_populates="claims")

    # Data Pemegang Polis
    nomor_polis = Column(String, nullable=False)
    nama_pemegang = Column(String, nullable=False)
    alamat_korespondensi = Column(String, nullable=False)
    kota_pemegang = Column(String, nullable=False)
    kode_pos_pemegang = Column(String, nullable=False)
    telp_rumah = Column(String)
    telp_kantor = Column(String)
    telp_hp = Column(String)
    email = Column(String)

    # Data Tertanggung
    nama_tertanggung = Column(String, nullable=False)
    tempat_lahir_tertanggung = Column(String, nullable=False)
    tanggal_lahir_tertanggung = Column(Date, nullable=False)
    jenis_kelamin = Column(String, nullable=False)
    pekerjaan_tertanggung = Column(String, nullable=False)
    nama_perusahaan = Column(String)
    kota_perusahaan = Column(String)
    kode_pos_perusahaan = Column(String)

    # Riwayat Penyakit / Cedera
    tanggal_perawatan = Column(Date, nullable=False)
    nama_dokter_rumah_sakit = Column(String, nullable=False)
    deskripsi_penyakit = Column(String, nullable=False)
    berhubungan_kecelakaan = Column(Boolean, nullable=False)
    tanggal_kecelakaan = Column(Date)

    # Claim Tracker
    status = Column(Enum(ClaimStatusEnum), default=ClaimStatusEnum.dikirim, nullable=False)
