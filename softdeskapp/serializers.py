from rest_framework.serializers import ModelSerializer, ValidationError

from .models import Project, Issue, Comment, Contributor


class IssueSerializer(ModelSerializer):
    class Meta:
        model = Issue
        fields = '__all__'
        # fields = ['title', 'desc', 'project', 'tag', 'priority', 'status', 'author_user',
        # 'assignee_user',
        # 'created_time']

    def validate_issue_name(self, value):
        if Issue.objects.filter(title=value).exists():
            raise ValidationError('Issue already exists')
        return value


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        # fields = ['description', 'issue', 'author_user', 'created_time']


class ContributorSerializer(ModelSerializer):
    class Meta:
        model = Contributor
        fields = '__all__'
        # fields = ['user', 'project', 'role']


class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        # fields = ['title', 'description', 'type', 'contributor']
        fields = '__all__'

    def validate_project_name(self, value):
        if Project.objects.filter(title=value).exists():
            raise ValidationError('Project already exists')
        return value


class ProjectDetailSerializer(ModelSerializer):
    project_contributor = ContributorSerializer(many=True)

    class Meta:
        model = Project
        fields = '__all__'
        # fields = ['title', 'description', 'type', 'project_contributor']
