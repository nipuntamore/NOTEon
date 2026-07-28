from django.db import models
#from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator

# Create your models here.
"""class User(AbstractUser):
    pass"""

class notes(models.Model):
    title = models.CharField()
    content = models.TextField()
    class priority_choices(models.TextChoices):
        High = 'high','HIGH'
        Medium = 'medium','MEDIUM'
        Low = 'low','LOW'
    priority = models.CharField(
        choices=priority_choices,
        default=priority_choices.Low
    )
    attachment = models.FileField(
        upload_to='attachments/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf','jpg','jpeg','png'])]
    )
    isarchived = models.BooleanField(
        default=False,
        null=True
    )

    def __str__(self):
        return self.title



