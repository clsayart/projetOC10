from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from authentication.models import User
from .models import Project, Contributor, Issue, Comment
from .serializers import ProjectSerializer, ProjectDetailSerializer, ContributorSerializer, IssueSerializer, \
    CommentSerializer
from .permissions import IsContributor, IsIssueAuthor, IsProjectAuthor


# VERIFIER LISTE WORD QUE CHAQUE ACTION FAIT BIEN CE QUI EST DEMANDE
class ProjectViewset(ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsContributor, IsProjectAuthor]

    def get_queryset(self):
        user = self.request.user
        projects = Project.objects.filter(contributor=user)
        return projects

    def create(self, request, *args, **kwargs):
        project_data = request.data
        serializer = ProjectDetailSerializer(data=project_data, partial=True)
        print("create")
        if serializer.is_valid():
            project = serializer.save()

            contributor = Contributor.objects.create(
                user=self.request.user,
                project=project,
                role='AUTHOR'
            )
            contributor.save()

            project.contributor.add(contributor.user)
            project.save()

            serializer = ProjectDetailSerializer(project)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        project = Project.objects.filter(pk=kwargs['pk'])
        if not project:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )
        project = project.get()

        project_data = request.data
        serializer = ProjectDetailSerializer(data=project_data, partial=True)

        if serializer.is_valid():
            if 'title' in project_data:
                project.title = project_data['title']
            if 'description' in project_data:
                project.description = project_data['description']
            if 'type' in project_data:
                project.type = project_data['type']

            project.save()
            serializer = ProjectDetailSerializer(project)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        project = Project.objects.filter(pk=kwargs['pk'])
        print("project", project)
        project = project.get()
        project.delete()
        # DOIT SUPPRIMER LES ISSUES AUSSI
        return Response(status=status.HTTP_204_NO_CONTENT)


class ContributorAPIView(APIView):
    permission_classes = (IsAuthenticated, IsContributor)

    def get(self, request, **kwargs):
        contributors = Contributor.objects.filter(project_id=kwargs['id'])
        serializers = ContributorSerializer(contributors, many=True)
        return Response(serializers.data)

    def post(self, request, **kwargs):
        project = Project.objects.filter(id=kwargs['id'])[0]
        contributor_data = request.data
        print("contributor_data", contributor_data)
        user = User.objects.get(pk=contributor_data['user'])

        serializer = ContributorSerializer(data=contributor_data, partial=True)
        print("create")
        if serializer.is_valid():
            contributor = Contributor.objects.create(
                user=user,
                project=project,
                role='CONTRIBUTOR'
            )
            contributor.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContributorDetailAPIView(APIView):
    permission_classes = (IsAuthenticated, IsContributor)

    def delete(self, request, **kwargs):
        contributor = Contributor.objects.filter(user=kwargs['user_id'], role='CONTRIBUTOR')
        # RAJOUT ROLE = CONTRIBUTOR DANS LE FILTER?
        print("kwargs['user_id']", kwargs['user_id'])
        print("contributor", contributor)

        contributor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class IssueAPIView(APIView):
    permission_classes = (IsAuthenticated, IsContributor)  # AUTRES?

    def get(self, request, **kwargs):
        issues = Issue.objects.filter(project_id=kwargs['project_id'])
        serializers = IssueSerializer(issues, many=True)
        return Response(serializers.data)

    def post(self, request, **kwargs):
        data = request.data
        print('data', data)
        project_id = kwargs['project_id']
        author_user = request.user

        if 'assignee_user' in data:
            user = User.objects.get(pk=data['assignee_user'])
            print("user", user)
            assignee_user = user.id
        else:
            assignee_user = request.user

        new_issue_data = {
            'title': data['title'],
            'desc': data['desc'],
            'tag': data['tag'],
            'priority': data['priority'],
            'status': data['status'],
            'author_user': author_user.id,
            'project': project_id,
            'assignee_user': assignee_user
        }
        serializer = IssueSerializer(data=new_issue_data, partial=True)
        if serializer.is_valid(project_id):
            new_issue = serializer.save()
            serializer = IssueSerializer(new_issue)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IssueDetailAPIView(APIView):
    permission_classes = (IsAuthenticated, IsContributor)

    def get(self, request, **kwargs):
        comment = Issue.objects.filter(id=self.kwargs['issue_id'])
        serializers = IssueSerializer(comment, many=True)
        return Response(serializers.data)

    def put(self, request, **kwargs):
        print("ici")
        issue = Issue.objects.filter(pk=kwargs['issue_id'], project=kwargs['p_id'])[0]
        print("issue", issue)
        issue_data = request.data
        print("issue data", issue_data)
        serializer = IssueSerializer(data=issue_data, partial=True)
        print("ici2")
        if serializer.is_valid():
            print("ici3")
            if 'title' in issue_data:
                issue.title = issue_data['title']
            if 'desc' in issue_data:
                issue.desc = issue_data['desc']
            if 'tag' in issue_data:
                issue.tag = issue_data['tag']
            if 'priority' in issue_data:
                issue.priority = issue_data['priority']
            if 'status' in issue_data:
                issue.status = issue_data['status']
            print("ici4")
            # if 'author_user' in issue_data:
            #     print("ici5")
            #     au_user = User.objects.get(pk=issue_data['author_user'])
            #     issue.author_user = au_user.id
            if 'assignee_user' in issue_data:
                as_user = User.objects.get(pk=issue_data['assignee_user'])
                print("as_user", as_user)
                issue.assignee_user = as_user
            print('issue', issue)
            issue.save()
            serializer = IssueSerializer(issue)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, **kwargs):
        # user, permissions?
        issue = Issue.objects.filter(pk=kwargs['issue_id'])
        issue.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentAPIView(APIView):
    permission_classes = (IsAuthenticated, IsContributor)

    def get(self, request, **kwargs):

        comments = Comment.objects.filter(issue_id=self.kwargs['issue_id'])
        serializers = CommentSerializer(comments, many=True)
        return Response(serializers.data)

    def post(self, request, **kwargs):
        data = request.data
        print('data', data)
        serializer = CommentSerializer(data=data, partial=True)

        if serializer.is_valid():
            comment_data = {}
            author_user = request.user
            print("author_user", author_user)
            issue = Issue.objects.get(pk=kwargs['issue_id'])

            comment_data['author_user'] = author_user.id
            comment_data['issue'] = issue.id
            comment_data['description'] = data['description']
            print("comment_data", comment_data)
            serializer = CommentSerializer(data=comment_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetailAPIView(APIView):
    permission_classes = (IsAuthenticated, IsContributor)

    def get(self, request, **kwargs):
        comments = Comment.objects.filter(id=self.kwargs['comment_id'])
        serializers = CommentSerializer(comments, many=True)
        return Response(serializers.data)

    def put(self, request, **kwargs):
        data = request.data
        print("comment_id", kwargs['comment_id'])
        comment = Comment.objects.filter(pk=kwargs['comment_id'])[0]
        print("comment", comment)
        serializer = CommentSerializer(data=data, partial=True)
        if serializer.is_valid():
            comment.description = data['description']
            comment.save()
            serializer = CommentSerializer(comment)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, **kwargs):
        user = request.user

        comment = Comment.objects.filter(pk=kwargs['comment_id'])
        comment.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT)
