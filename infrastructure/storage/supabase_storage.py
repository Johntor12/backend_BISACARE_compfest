import os
from supabase import create_client, Client
from fastapi import UploadFile
from uuid import uuid4



class SupabaseStorage:
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")  # pakai service role key
        self.bucket = os.getenv("SUPABASE_BUCKET", "insurance-forms")
        self.client: Client = create_client(self.url, self.key)

        if not self.url or not self.key:
            raise RuntimeError("Supabase ENV variables is missing!")

    async def upload_file(self, file: UploadFile, prefix: str) -> str:
        ext = file.filename.split(".")[-1]
        unique_name = f"{prefix}_{uuid4().hex}.{ext}"
        file_bytes = await file.read()

        # Upload ke Supabase bucket
        self.client.storage.from_(self.bucket).upload(unique_name, file_bytes, {"content-type": file.content_type})

        # Ambil URL (kalau bucket public)
        public_url = self.client.storage.from_(self.bucket).get_public_url(unique_name)
        # if isinstance(public_url, dict):
            # supabase-py older/newer differences, try common keys
            # return public_url.get("publicUrl") or public_url.get("public_url") or public_url.get("url") or str(public_url)
        return public_url

    def generate_signed_url(self, filename: str, expires_in: int = 3600) -> str:
        """Hanya untuk bucket private"""
        res = self.client.storage.from_(self.bucket).create_signed_url(filename, expires_in)
        return res.get("signedURL")
