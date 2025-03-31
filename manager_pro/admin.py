from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Team,
    Project,
    Position,
    TaskType,
    Worker
)


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    pass


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    pass


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    pass


admin.site.register(Position)


admin.site.register(TaskType)