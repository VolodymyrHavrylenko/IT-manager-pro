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
        team_name = self.team.name if self.team else "Without a team"
        position_name = self.position.name if self.position else "No position"
        return (
            f"{self.first_name} "
            f"{self.last_name} | "
            f"{team_name} ({position_name})"
        )


class Project(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True
    )
    description = models.TextField(blank=True)
    team = models.ManyToManyField(
        Team,
        related_name="projects",
        blank=True)

    def __str__(self):
        return self.name


class TaskType(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True
    )

    def __str__(self):
        return self.name


class Task(models.Model):
    class Priority(models.TextChoices):
        LOW = "low"
        MEDIUM = "medium"
        HIGH = "high"
        CRITICAL = "critical"

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    deadline = models.DateTimeField()
    is_complete = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=10,
        choices=Priority.choices,
        default=Priority.MEDIUM
    )
    task_type = models.ForeignKey(
        TaskType,
        on_delete=models.SET_NULL,
        null=True,
        related_name="tasks",
    )
    assigned_to = models.ForeignKey(
        Worker,
        on_delete=models.SET_NULL,
        null=True,
        related_name="assigned_tasks"
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="tasks",
    )

    def __str__(self):
        assigned = self.assigned_to.get_full_name() if self.assigned_to else "Not Assigned"
        return (
            f"{self.name} ({self.get_priority_display()}) | "
            f"Deadline: {self.deadline.strftime('%Y-%m-%d')} | "
            f"Assigned to: {assigned} | "
            f"{'✅ Completed' if self.is_complete else '❌ In Progress'}"
        )
