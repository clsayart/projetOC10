from django.db import models

from softdesk import settings


class Project(models.Model):
    BACKEND = "BACK-END"
    FRONTEND = "FRONT-END"
    IOS = "IOS"
    ANDROID = "ANDROID"

    TYPE_CHOICES = [
        (BACKEND, 'back-end'),
        (FRONTEND, 'front-end'),
        (IOS, 'iOS'),
        (ANDROID, 'Android'),
    ]
    title = models.CharField(max_length=200, blank=False)
    description = models.CharField(max_length=5000)
    type = models.CharField(max_length=200, choices=TYPE_CHOICES, blank=False)
    contributor = models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='Contributor',
                                         related_name='project_contributed')

    def __str__(self):
        return self.title


class Contributor(models.Model):
    AUTHOR = 'AUTHOR'
    CONTRIBUTOR = 'CONTRIBUTOR'

    CHOICES = [
        (AUTHOR, 'Author'),
        (CONTRIBUTOR, 'Contributor'),
    ]

    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE, related_name='project_contributor')
    role = models.CharField(max_length=30, choices=CHOICES)

    def __str__(self):
        return self.user.first_name


class Issue(models.Model):
    FAIBLE = "FAIBLE"
    MOYENNE = "MOYENNE"
    ELEVEE = "HIGH"
    BUG = "BUG"
    AMELIORATION = "IMPROVEMENT"
    TACHE = "TASK"
    A_FAIRE = "TODO"
    EN_COURS = "IN_PROGRESS"
    TERMINE = "COMPLETED"

    PRIORITY_CHOICES = [
        (FAIBLE, 'Faible'),
        (MOYENNE, 'Moyenne'),
        (ELEVEE, 'Elevée'),
    ]

    TAG_CHOICES = [
        (BUG, "Bug"),
        (AMELIORATION, "Amélioration"),
        (TACHE, "Tâche"),
    ]

    STATUS_CHOICES = [
        (A_FAIRE, "A faire"),
        (EN_COURS, "En cours"),
        (TERMINE, "Terminé"),
    ]

    title = models.CharField(max_length=200)
    desc = models.CharField(max_length=5000)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    tag = models.CharField(max_length=30, choices=TAG_CHOICES)
    priority = models.CharField(max_length=30, choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES)

    author_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='author')
    assignee_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, null=True,
                                      related_name='assignee')

    created_time = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    description = models.CharField(max_length=5000, blank=False)
    author_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.RESTRICT)
    issue = models.ForeignKey(to=Issue, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
