import os

from fastapi import UploadFile
from dependency_injector.wiring import inject, Provide

from app.components.media.exceptions import InvalidMediaException
from app.components.media.utils import normalize_filename
from app.configs import MediaConfig
from app.containers import Container, container

@inject
def validate_media(
    file: UploadFile,
    config: MediaConfig = Provide[Container.config.provided.media]
) -> str:
    if file.content_type not in config.allowed_file_types:
        raise InvalidMediaException(
            f"Invalid file type: {file.content_type}. "
            f"Allowed: {', '.join(config.allowed_file_types)}."
        )
    
    if file.size > config.max_file_size_mb * 1024 * 1024:
        raise InvalidMediaException(
            "File is too large. Max size: "
            f"{config.max_file_size_mb} MB."
        )

    media_dir = os.path.join(*config.media_dir)
    if not os.path.exists(media_dir):
        os.makedirs(media_dir, exist_ok=True)
    valid_file_name = normalize_filename(file.filename)
    return (
        os.path.join(media_dir, valid_file_name),
        config.media_endpoint + valid_file_name
    )

container.wire(modules=[__name__])
