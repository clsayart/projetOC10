from rest_framework.serializers import ModelSerializer

from .models import Project, Issue, Comment, Contributor


class IssueSerializer(ModelSerializer):
    class Meta:
        model = Issue
        fields = ['title', 'desc', 'project', 'tag', 'priority', 'status', 'author_user',
                  'assignee_user',
                  'created_time']


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['description', 'issue', 'author_user', 'created_time']


class ContributorSerializer(ModelSerializer):
    class Meta:
        model = Contributor
        fields = ['user', 'project', 'role']


class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ['title', 'description', 'type', 'contributor']


class ProjectDetailSerializer(ModelSerializer):
    project_contributor = ContributorSerializer(many=True)

    class Meta:
        model = Project
        fields = ['title', 'description', 'type', 'project_contributor']
