# from domain.models.claim import Claim
# from infrastructure.d import get_db

# class ClaimUseCase:
#     def __init__(self, db):
#         self.db = db

#     def create_claim(self, data):
#         new_claim = Claim(**data)
#         self.db.add(new_claim)
#         self.db.commit()
#         self.db.refresh(new_claim)
#         return new_claim