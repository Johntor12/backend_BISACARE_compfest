from domain.entities.claim import Claim
from infrastructure.db.repositories.claim_repository import ClaimRepository

class ClaimService:
    def __init__(self, claim_repository: ClaimRepository):
        self.claim_repository = claim_repository

    async def create_claim(self, claim: Claim):
        return await self.claim_repository.create_claim(claim)

    async def get_all_claims(self):
        return await self.claim_repository.get_all_claims()

    async def get_claim_by_id(self, claim_id: int):
        return await self.claim_repository.get_claim_by_id(claim_id)

    async def update_claim(self, claim_id: int, claim: Claim):
        return await self.claim_repository.update_claim(claim_id, claim)

    async def delete_claim(self, claim_id: int):
        return await self.claim_repository.delete_claim(claim_id)
