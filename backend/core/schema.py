import graphene
from graphene_django.types import DjangoObjectType
from .models import Organization, Project, Task, TaskComment

class OrganizationType(DjangoObjectType):
    class Meta:
        model = Organization
        fields = ("id", "name", "slug", "contact_email")


class ProjectType(DjangoObjectType):
    class Meta:
        model = Project
        fields = ("id", "organization", "name", "description", "status", "due_date")


class TaskCommentType(DjangoObjectType):
    class Meta:
        model = TaskComment
        fields = ("id", "content", "author_email", "timestamp")

class TaskType(DjangoObjectType):
    comments = graphene.List(TaskCommentType)

    class Meta:
        model = Task
        fields = ("id", "title", "description", "status", "assignee_email", "due_date", "comments")

    def resolve_comments(self, info):
        return self.comments.all()
    

class ProjectType(DjangoObjectType):
    tasks = graphene.List(TaskType)

    class Meta:
        model = Project
        fields = ("id", "name", "description", "status", "due_date", "tasks")

    def resolve_tasks(self, info):
        return self.tasks.all()
 

class Query(graphene.ObjectType):
    organizations = graphene.List(OrganizationType)
    projects = graphene.List(ProjectType)
    tasks = graphene.List(TaskType)
    task_comments = graphene.List(TaskCommentType)

    def resolve_organizations(root, info):
        return Organization.objects.all()

    def resolve_projects(root, info):
        return Project.objects.all()

    def resolve_tasks(root, info):
        return Task.objects.all()

    def resolve_task_comments(root, info):
        return TaskComment.objects.all()


# Create Project
class CreateProject(graphene.Mutation):
    class Arguments:
        organization_id = graphene.ID(required=True)
        name = graphene.String(required=True)
        description = graphene.String()
        status = graphene.String()
        due_date = graphene.types.datetime.Date()

    project = graphene.Field(ProjectType)

    def mutate(root, info, organization_id, name, description="", status="ACTIVE", due_date=None):
        org = Organization.objects.get(id=organization_id)
        project = Project.objects.create(
            organization=org,
            name=name,
            description=description,
            status=status,
            due_date=due_date
        )
        return CreateProject(project=project)

# Update Project
class UpdateProject(graphene.Mutation):
    class Arguments:
        project_id = graphene.ID(required=True)
        name = graphene.String()
        description = graphene.String()
        status = graphene.String()
        due_date = graphene.types.datetime.Date()

    project = graphene.Field(ProjectType)

    def mutate(root, info, project_id, **kwargs):
        project = Project.objects.get(id=project_id)
        for key, value in kwargs.items():
            setattr(project, key, value)
        project.save()
        return UpdateProject(project=project)

# Create Task
class CreateTask(graphene.Mutation):
    class Arguments:
        project_id = graphene.ID(required=True)
        title = graphene.String(required=True)
        description = graphene.String()
        status = graphene.String()
        assignee_email = graphene.String()
        due_date = graphene.types.datetime.DateTime()

    task = graphene.Field(TaskType)

    def mutate(root, info, project_id, title, **kwargs):
        project = Project.objects.get(id=project_id)
        task = Task.objects.create(project=project, title=title, **kwargs)
        return CreateTask(task=task)

# Update Task
class UpdateTask(graphene.Mutation):
    class Arguments:
        task_id = graphene.ID(required=True)
        title = graphene.String()
        description = graphene.String()
        status = graphene.String()
        assignee_email = graphene.String()
        due_date = graphene.types.datetime.DateTime()

    task = graphene.Field(TaskType)

    def mutate(root, info, task_id, **kwargs):
        task = Task.objects.get(id=task_id)
        for key, value in kwargs.items():
            setattr(task, key, value)
        task.save()
        return UpdateTask(task=task)

# Create Comment
class CreateTaskComment(graphene.Mutation):
    class Arguments:
        task_id = graphene.ID(required=True)
        content = graphene.String(required=True)
        author_email = graphene.String(required=True)

    comment = graphene.Field(TaskCommentType)

    def mutate(root, info, task_id, content, author_email):
        task = Task.objects.get(id=task_id)
        comment = TaskComment.objects.create(
            task=task,
            content=content,
            author_email=author_email
        )
        return CreateTaskComment(comment=comment)

class Mutation(graphene.ObjectType):
    create_project = CreateProject.Field()
    update_project = UpdateProject.Field()
    create_task = CreateTask.Field()
    update_task = UpdateTask.Field()
    create_task_comment = CreateTaskComment.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
