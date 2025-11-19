import string
import random
from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User   # <-- add this


def generate_random_slug(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


class ShortURL(models.Model):
    user = models.ForeignKey(    # <-- new
        User,
        on_delete=models.CASCADE,
        related_name='short_urls',
        null=True,
        blank=True,
    )
    slug = models.SlugField(
        max_length=10,
        unique=True,
        blank=True,
        help_text="Leave empty to auto-generate."
    )
    target_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    clicks = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            new_slug = generate_random_slug()
            while ShortURL.objects.filter(slug=new_slug).exists():
                new_slug = generate_random_slug()
            self.slug = new_slug
        else:
            self.slug = slugify(self.slug)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.slug} → {self.target_url}"
