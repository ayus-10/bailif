from pydantic import BaseModel


class IssuedRefreshToken(BaseModel):
    selector: str
    verifier_hash: str
    full_token: str
