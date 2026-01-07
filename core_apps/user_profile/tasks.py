import base64
from uuid import UUID

import cloudinary.uploader
from celery import shared_task
from django.apps import apps
from django.core.files.storage import default_storage
from loguru import logger


@shared_task(
    name="upload_photos_to_cloudinary",
    # soft_time_limit=60,
    # time_limit=90,
)
def upload_photos_to_cloudinary(profile_id: str, photos: dict) -> None:
    try:
        profile_model = apps.get_model("user_profile", "Profile")
        profile = profile_model.objects.get(id=profile_id)

        for field_name, photo_data in photos.items():

            if photo_data["type"] == "base64":
                # ✅ BASE64 PATH
                image_bytes = base64.b64decode(photo_data["data"])
                response = cloudinary.uploader.upload(
                    image_bytes,
                    resource_type="image",
                    folder="profiles"
                )

            elif photo_data["type"] == "file":
                # ✅ FILE PATH
                file_path = photo_data["path"]

                if not default_storage.exists(file_path):
                    logger.error(f"File not found: {file_path}")
                    continue

                with open(file_path, "rb") as image_file:
                    response = cloudinary.uploader.upload(
                        image_file,
                        resource_type="image",
                        folder="profiles"
                    )

                default_storage.delete(file_path)

            else:
                logger.error(f"Unknown photo type: {photo_data}")
                continue

            setattr(profile, field_name, response["public_id"])
            setattr(profile, f"{field_name}_url", response["secure_url"])

        profile.save()
        logger.info(f"Photos uploaded for {profile.user.email}")

    except Exception as e:
        logger.exception(
            f"Failed to upload photos for profile {profile_id}: {str(e)}"
        )