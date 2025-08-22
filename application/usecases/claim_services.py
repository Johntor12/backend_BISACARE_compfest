from domain.entities.claim import Claim
from infrastructure.db.repositories.claim_repository import ClaimRepository
from fastapi import HTTPException

class ClaimService:
    def __init__(self, claim_repository: ClaimRepository):
        self.claim_repository = claim_repository

    async def create_claim(self, user_id: int, status: str) -> Claim:
        new_claim = Claim(id=None, user_id=user_id, status=status)

        return await self.claim_repository.create_claim(new_claim)

    async def get_all_claims(self):
        return await self.claim_repository.get_all_claims()

    async def get_claim_by_id(self, claim_id: int) -> Claim:
        existing_claim = await self.claim_repository.get_claim_by_id(claim_id)
        if not existing_claim:
            raise HTTPException(status_code=404, detail="Claim tidak ditemukan")
        
        return await self.claim_repository.get_claim_by_id
    
    async def get_claim_by_user(self, user_id: int) -> Claim:
        existing_claim = await self.claim_repository.get_claim_by_user(user_id)
        if not existing_claim:
            raise HTTPException

    async def update_claim(self, claim_id: int, claim: Claim):
        existing_claim = await self.claim_repository.get_claim_by_id(claim_id)
        if not existing_claim:
            raise HTTPException(status_code=404, detail="Claim tidak ditemukan")

        return await self.claim_repository.update_claim(claim_id, claim)

    async def delete_claim(self, claim_id: int):
        return await self.claim_repository.delete_claim(claim_id)
    
    # Fitur untuk Claim Tracker, Slip digital, dan claim progress

    async def get_claim_tracker(self, user_id: int):
        claims = await self.claim_repository.get_claims_by_user_id(user_id)
        tracker_list=[]
        for claim in claims:
            events = await self.claim_repository.get_claim_event_by_claim_id(claim.id)
            tracker_list.append({
                "claim_id": claim.id,
                "status": claim.status,
                "events": [{"step": e.step, "status": e.status, "timestamp": e.timestamp} for e in events]
            })
        return tracker_list
    
    async def get_slip_digital(self, claim_id: int):
        claim_doc = await self.claim_repository.get_claim_document_by_claim_id(claim_id)
        if not claim_doc or not claim_doc.file_url:
            raise HTTPException(status_code=404, detail="Slip digital tidak ditemukan")
        return {
            "claim_id": claim_id,
            "file_url": claim_doc.file_url,
            "file_type": claim_doc.file_type,
            "uploaded_at": claim_doc.uploaded_at
        }

    async def get_claim_progress(self, claim_id: int):
        events = await self.claim_repository.get_claim_event_by_claim_id(claim_id)
        if not events:
            return {"claim_id": claim_id, "progress": 0}
        completed_steps = sum(1 for e in events if e.status.lower() in ("selesai", "diterima"))
        total_steps = len(events)
        progress_percentage = round((completed_steps / total_steps) * 100, 2) if total_steps else 0
        return {"claim_id": claim_id, "progress": progress_percentage}
