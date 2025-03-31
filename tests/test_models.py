from django.test import TestCase
from manager_pro.models import Position, Team, Worker, Project, TaskType, Task
from django.utils import timezone


class PositionModelTest(TestCase):
    def test_position_str(self):
        position = Position.objects.create(name="Developer")
        self.assertEqual(str(position), "Developer")


class TeamModelTest(TestCase):
    def test_team_str(self):
        team = Team.objects.create(name="Backend Team")
        self.assertEqual(str(team), "Backend Team")


class WorkerModelTest(TestCase):
    def test_worker_str(self):
        position = Position.objects.create(name="Developer")
        team = Team.objects.create(name="Backend Team")
        worker = Worker.objects.create(
            username="john_doe",
            first_name="John",
            last_name="Doe",
            position=position,
            team=team,
        )
        self.assertEqual(str(worker), "John Doe | Backend Team (Developer)")


class ProjectModelTest(TestCase):
    def test_project_str(self):
        project = Project.objects.create(
            name="Project Alpha", description="A new project"
        )
        self.assertEqual(str(project), "Project Alpha")


class TaskModelTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Developer")
        self.team = Team.objects.create(name="Backend Team")
        self.worker = Worker.objects.create(
            username="john_doe",
            first_name="John",
            last_name="Doe",
            position=self.position,
            team=self.team
        )
        self.task_type = TaskType.objects.create(name="Bug")
        self.project = Project.objects.create(name="Project Alpha", description="A new project")
        self.task = Task.objects.create(
            name="Fix bug",
            description="Fix the bug in the system",
            deadline=timezone.now() + timezone.timedelta(days=5),
            priority=Task.Priority.HIGH,
            task_type=self.task_type,
            assigned_to=self.worker,
            project=self.project,
            is_complete=False
        )

    def test_task_str_in_progress(self):
        self.assertEqual(
            str(self.task),
            f"Fix bug ({self.task.get_priority_display()}) | "
            f"Deadline: {self.task.deadline.strftime('%Y-%m-%d')} | "
            f"Assigned to: John Doe | "
            f"❌ In Progress"
        )

    def test_task_str_completed(self):
        self.task.is_complete = True
        self.task.save()
        self.assertEqual(
            str(self.task),
            f"Fix bug ({self.task.get_priority_display()}) | "
            f"Deadline: {self.task.deadline.strftime('%Y-%m-%d')} | "
            f"Assigned to: John Doe | "
            f"✅ Completed"
        )

    def test_task_priority_choices(self):
        task = Task.objects.create(
            name="Fix bug",
            description="Fix the bug in the system",
            deadline=timezone.now() + timezone.timedelta(days=5),
            priority=Task.Priority.LOW,
            project=self.project,
        )
        self.assertEqual(task.priority, Task.Priority.LOW)

    def test_task_completion_status(self):
        self.assertFalse(self.task.is_complete)

        self.task.is_complete = True
        self.task.save()

        self.task.refresh_from_db()
        self.assertTrue(self.task.is_complete)
