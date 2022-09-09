from rest_framework.permissions import BasePermission

from .models import Contributor, Issue


class IsContributor(BasePermission):

    def has_contributor_permission(self, request, view):

        user = request.user
        project_id = view.kwargs['project_id']

        contributor = Contributor.objects.filter(project=project_id, user=user.id)

        if not contributor:
            return False
        else:
            return True


class IsProjectAuthor(BasePermission):
    message = "You are not the author. You cannot update or delete a project"

    def has_permission(self, request, view):
        if view.action in ['create', 'list', 'retrieve']:
            return True
        if view.action in ['put', 'destroy']:
            user = request.user
            if not 'project_id' in view.kwargs:
                project_id = view.kwargs['pk']
            else:
                project_id = view.kwargs['project_id']
            author = Contributor.objects.filter(project=project_id, user=user.id, role='AUTHOR')
            print('project author in permission - author', author)
            if not author:
                return False
            return True


class IsIssueAuthor(BasePermission):

    message = "You are not the author. You cannot update or delete an issue"

    def has_permission(self, request, view):
        if view.action in ['create', 'list', 'retrieve']:
            return True
        if view.action in ['update', 'destroy']:
            user = request.user
            if not 'issue_id' in view.kwargs:
                issue_id = view.kwargs['pk']
            else:
                issue_id = view.kwargs['issue_id']
            author = Issue.objects.filter(id=issue_id, author_user=user.id)
            if not author:
                return False
            return True

