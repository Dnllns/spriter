import uuid

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status

from ..application.dto import AddVersionRequest, CreateSpriteRequest
from ..application.services import SpriteService
from ..dependencies import get_current_user, get_service
from ..domain.entities import Sprite, SpriteVersion, User

router = APIRouter(tags=["sprites"])


@router.post("/sprites", status_code=status.HTTP_201_CREATED, response_model=Sprite)
async def create_sprite(
    request: CreateSpriteRequest,
    service: SpriteService = Depends(get_service),
    current_user: User = Depends(get_current_user),
):
    return await service.create_new_sprite(request, current_user.id)


@router.get("/sprites", response_model=list[Sprite])
async def list_sprites(
    limit: int = 10, offset: int = 0, service: SpriteService = Depends(get_service)
):
    return await service.list_sprites(limit, offset)


@router.get("/sprites/{sprite_id}", response_model=Sprite)
async def get_sprite(
    sprite_id: uuid.UUID, service: SpriteService = Depends(get_service)
):
    sprite = await service.get_sprite(sprite_id)
    if not sprite:
        raise HTTPException(status_code=404, detail="Sprite not found")
    return sprite


@router.post(
    "/sprites/{sprite_id}/versions",
    status_code=status.HTTP_201_CREATED,
    response_model=SpriteVersion,
)
async def add_sprite_version(
    sprite_id: uuid.UUID,
    file: UploadFile = File(...),
    metadata: str = Form("{}"),  # JSON string
    changelog: str = Form(None),
    service: SpriteService = Depends(get_service),
    current_user: User = Depends(get_current_user),
):
    import json

    sprite = await service.get_sprite(sprite_id)
    if not sprite:
        raise HTTPException(status_code=404, detail="Sprite not found")

    if sprite.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to update this sprite",
        )

    try:
        meta_dict = json.loads(metadata)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid metadata JSON") from None

    file_content = await file.read()
    request = AddVersionRequest(metadata=meta_dict, changelog=changelog)

    version = await service.add_sprite_version(sprite_id, file_content, request)
    if not version:
        raise HTTPException(status_code=404, detail="Sprite not found")
    return version
