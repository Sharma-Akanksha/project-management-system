import graphene
from graphene_django.types import DjangoObjectType
from .models import Organization, Project, Task, TaskComment

class OrganizationType(DjangoObjectType):
    class Meta:
        model = Organization
        fields = ("id", "name", "slug", "contact_email")

class ProjectType(DjangoObjectType):
    task_count = graphene.Int()
    completed_tasks = graphene.Int()
    completion_rate = graphene.Float()

    class Meta:
        model = Project
        fields = ("id", "name", "description", "status", "due_date", "organization", "tasks")

    def resolve_task_count(self, info):
        return self.tasks.count()

    def resolve_completed_tasks(self, info):
        return self.tasks.filter(status="DONE").count()

    def resolve_organization(self, info):
        return self.organization
    
    def resolve_completion_rate(self, info):
        total = self.tasks.count()
        if total == 0:
            return 0.0
        done = self.tasks.filter(status="DONE").count()
        return round((done / total) * 100, 2)

class TaskCommentType(DjangoObjectType):
    created_at = graphene.DateTime()

    class Meta:
        model = TaskComment
        fields = (
            "id",
            "content",
            "author_email",
            "created_at",
            "task",
        )
    

class TaskType(DjangoObjectType):
    comments = graphene.List(TaskCommentType)

    class Meta:
        model = Task
        fields = (
            "id",
            "title",
            "description",
            "status",
            "assignee_email",
            "due_date",
            "created_at",
            "project",
        )
        
    def resolve_comments(self, info):
        return self.comments.all()
    

class Query(graphene.ObjectType):
    organizations = graphene.List(OrganizationType)
    projects = graphene.List(ProjectType, organization_slug=graphene.String(required=False))
    tasks = graphene.List(
        TaskType,
        project_id=graphene.ID(required=True),
        organization_slug=graphene.String(required=True),
    )
    task_comments = graphene.List(
        TaskCommentType,
        task_id=graphene.ID(required=True),
        organization_slug=graphene.String(required=True),
    )

    def resolve_projects(self, info, organization_slug):
        try:
            org = Organization.objects.get(slug=organization_slug)
            return Project.objects.filter(organization=org)
        except Organization.DoesNotExist:
            return Project.objects.none()


    # def resolve_projects(self, info, organization_slug=None):
    #     if organization_slug:
    #         organization = Organization.objects.filter(slug=organization_slug).first()
    #     else:
    #         organization = Organization.objects.first()

    #     if not organization:
    #         return Project.objects.none()

    #     return Project.objects.filter(organization=organization)


    def resolve_tasks(self, info, project_id, organization_slug):
        return Task.objects.filter(
            project__id=project_id,
            project__organization__slug=organization_slug,
        )

    def resolve_task_comments(self, info, task_id, organization_slug):
        return TaskComment.objects.filter(
            task__id=task_id,
            task__project__organization__slug=organization_slug,
        ).order_by("created_at")


# Create Project
# class CreateProject(graphene.Mutation):
#     class Arguments:
#         organization_slug = graphene.String(required=True)
#         # organization_id = graphene.ID(required=True)
#         name = graphene.String(required=True)
#         description = graphene.String()
#         status = graphene.String()
#         due_date = graphene.types.datetime.Date()

#     project = graphene.Field(ProjectType)

#     def mutate(root, info, organization_id, name, description="", status="ACTIVE", due_date=None):
#         org = Organization.objects.get(id=organization_id)
#         project = Project.objects.create(
#             organization=org,
#             name=name,
#             description=description,
#             status=status,
#             due_date=due_date
#         )
#         return CreateProject(project=project)

class CreateProject(graphene.Mutation):
    project = graphene.Field(ProjectType)

    class Arguments:
        organization_slug = graphene.String(required=True)
        name = graphene.String(required=True)
        description = graphene.String()
        status = graphene.String()
        due_date = graphene.Date()

    def mutate(self, info, organization_slug, name, description="", status="ACTIVE", due_date=None):
        try:
            org = Organization.objects.get(slug=organization_slug)
        except Organization.DoesNotExist:
            raise Exception("Organization not found")

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
    task = graphene.Field(TaskType)

    class Arguments:
        project_id = graphene.ID(required=True)
        organization_slug = graphene.String(required=True)
        title = graphene.String(required=True)
        description = graphene.String()
        status = graphene.String(required=True)
        assignee_email = graphene.String()
        due_date = graphene.DateTime()

    def mutate(
        self,
        info,
        project_id,
        organization_slug,
        title,
        status,
        description="",
        assignee_email="",
        due_date=None,
    ):
        project = Project.objects.get(
            id=project_id,
            organization__slug=organization_slug,
        )

        task = Task.objects.create(
            project=project,
            title=title,
            description=description,
            status=status,
            assignee_email=assignee_email,
            due_date=due_date,
        )

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

# Update Task Status
class UpdateTaskStatus(graphene.Mutation):
    class Arguments:
        task_id = graphene.ID(required=True)
        status = graphene.String(required=True)

    task = graphene.Field(TaskType)

    def mutate(root, info, task_id, status):
        task = Task.objects.get(id=task_id)
        task.status = status
        task.save()
        return UpdateTaskStatus(task=task)

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
    update_task_status = UpdateTaskStatus.Field()
    create_task_comment = CreateTaskComment.Field()
 

schema = graphene.Schema(query=Query, mutation=Mutation)
