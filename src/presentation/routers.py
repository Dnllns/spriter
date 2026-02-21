import uuid

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    Query,
    UploadFile,
    status,
)

from ..application.dto import AddVersionRequest, CreateSpriteRequest
from ..application.services import SpriteService
from ..dependencies import get_current_user, get_current_user_optional, get_service
from ..domain.entities import Sprite, SpriteVersion, User
from ..domain.exceptions import UnauthorizedError

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
    limit: int = Query(10, gt=0, le=100),
    offset: int = Query(0, ge=0),
    service: SpriteService = Depends(get_service),
    current_user: User | None = Depends(get_current_user_optional),
):
    only_public = current_user is None
    return await service.list_sprites(limit, offset, only_public=only_public)


@router.get("/sprites/{sprite_id}", response_model=Sprite)
async def get_sprite(
    sprite_id: uuid.UUID,
    service: SpriteService = Depends(get_service),
    current_user: User | None = Depends(get_current_user_optional),
):
    sprite = await service.get_sprite(sprite_id)
    if not sprite.is_public and (
        not current_user or sprite.author_id != current_user.id
    ):
        raise UnauthorizedError("You are not allowed to view this private sprite")
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
    animations: str = Form("[]"),  # JSON string
    changelog: str = Form(None),
    service: SpriteService = Depends(get_service),
    current_user: User = Depends(get_current_user),
):
    import json

    sprite = await service.get_sprite(sprite_id)
    if sprite.author_id != current_user.id:
        raise UnauthorizedError("You are not allowed to update this sprite")

    try:
        meta_dict = json.loads(metadata)
        anim_list = json.loads(animations)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=400, detail="Invalid JSON format in form"
        ) from None

    file_content = await file.read()
    request = AddVersionRequest(
        metadata=meta_dict, animations=anim_list, changelog=changelog
    )

    version = await service.add_sprite_version(sprite_id, file_content, request)
    return version
