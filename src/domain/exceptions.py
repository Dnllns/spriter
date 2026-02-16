class DomainError(Exception):
    """Base class for domain exceptions"""

    pass


class SpriteNotFoundError(DomainError):
    def __init__(self, sprite_id):
        self.sprite_id = sprite_id
        self.message = f"Sprite {sprite_id} not found"
        super().__init__(self.message)


class UnauthorizedError(DomainError):
    def __init__(self, message="Not authorized"):
        self.message = message
        super().__init__(self.message)
