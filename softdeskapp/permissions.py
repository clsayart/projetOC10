from rest_framework.permissions import BasePermission
from rest_framework import permissions

from .models import Contributor, Issue, Comment


class IsContributor(BasePermission):

    def has_contributor_permission(self, request, view):

        print('IsContributor')
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
        print(' you are in IsProjectAuthor')
        print("view", view)
        print("view.action is", view.action)
        print("view.kwargs is", view.kwargs)
        if view.action in ['create', 'list', 'retrieve']:
            return True
        if view.action in ['update', 'destroy']:
            print('update', 'destroy')
            user = request.user
            if not 'project_id' in view.kwargs:
                project_id = view.kwargs['pk']
            else:
                project_id = view.kwargs['project_id']
            author = Contributor.objects.filter(project=project_id, user=user.id, role='AUTHOR')
            contributor = Contributor.objects.filter(project=project_id, user=user.id, role='CONTRIBUTOR')
            print('project author in permission - author', author, contributor)
            if not author:
                return False
            return True


class IsIssueAuthor(BasePermission):
    message = "You are not the author. You cannot update or delete an issue"
    edit_safe_methods = ("GET", "POST")
    edit_methods = ("PUT", "DELETE")

    def has_permission(self, request, view):
        print("view", view)
        # print("view.action", view.action)
        print("view.kwargs", view.kwargs)
        print("permissions.SAFE_METHODS", permissions.SAFE_METHODS)
        print("request.method", request.method)
        if request.method in self.edit_safe_methods:
            return True
        if request.method in self.edit_methods:
            user = request.user
            print("user", user)
            if not 'issue_id' in view.kwargs:
                issue_id = view.kwargs['pk']
            else:
                issue_id = view.kwargs['issue_id']
            print("issue_id, user.id", issue_id, user.id)
            issue_author = Issue.objects.filter(id=issue_id, author_user=user.id)
            # author = Issue.objects.filter(pk=issue_id, author_user=user.id)
            print("issue_author", issue_author)
            if not issue_author:
                return False
            return True


class IsCommentAuthor(BasePermission):
    message = "You are not the author. You cannot update or delete a comment"
    edit_safe_methods = ("GET", "POST")
    edit_methods = ("PUT", "DELETE")

    def has_permission(self, request, view):
        print("view comment", view)
        print("view.kwargs", view.kwargs)
        print("request.method", request.method)
        if request.method in self.edit_safe_methods:
            return True
        if request.method in self.edit_methods:
            user = request.user
            print("user", user)
            if not 'comment_id' in view.kwargs:
                comment_id = view.kwargs['pk']
            else:
                comment_id = view.kwargs['comment_id']
            print("comment_id, user.id", comment_id, user.id)
            comment_author = Comment.objects.filter(id=comment_id, author_user=user.id)
            print("comment_author", comment_author)
            if not comment_author:
                return False
            return True
        # print("view comment", view)
        # print("view.kwargs", view.kwargs)
        # if view.action in ['create', 'list', 'retrieve']:
        #     return True
        # if view.action in ['update', 'destroy']:
        #     user = request.user
        #     if not 'comment_id' in view.kwargs:
        #         comment_id = view.kwargs['pk']
        #     else:
        #         comment_id = view.kwargs['comment_id']
        #     author = Comment.objects.filter(id=comment_id, author_user=user.id)
        #     if not author:
        #         return False
        #     return True
