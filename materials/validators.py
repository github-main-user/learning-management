from urllib.parse import urlparse

from rest_framework.validators import ValidationError


class AllowedURLValidator:
    """Validates if given URL contains youtube.com domain."""

    def __call__(self, value):
        parsed = urlparse(value)
        if "youtube.com" not in parsed.netloc:
            raise ValidationError("Only links on youtube.com are allowed")
