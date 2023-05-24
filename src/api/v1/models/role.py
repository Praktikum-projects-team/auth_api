from pydantic import BaseModel, UUID4


class RoleBase(BaseModel):
    id: UUID4
    name: str


class RoleName(BaseModel):
    name: str


class RoleUser(BaseModel):
    user_id: UUID4
    role_id: UUID4
