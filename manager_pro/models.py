from django.contrib.auth.models import AbstractUser
from django.db import models


class Position(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True
    )

    def __str__(self):
        return self.name



class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="workers",
    )
    team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="workers",
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} Team: {self.team} ({self.position})"


