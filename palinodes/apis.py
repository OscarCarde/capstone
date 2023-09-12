import json

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from palinodes.helpers import send_notifications

from .models import Directory, User, FileModel, Comment
from .serializers import CommentSerializer, NotificationSerializer, DirectorySerializer, FileSerializer, UserSerializer

@login_required
def add_collaborator_api(request):
    raw_content = request.body
    loaded_content = json.loads(raw_content)
    new_collaboratorpk = loaded_content.get("newCollaboratorpk")
    repositorypk = loaded_content.get("repositorypk")

    try:
        repository = Directory.objects.get(pk=repositorypk)
        new_collaborator = User.objects.get(pk=new_collaboratorpk)

        repository.collaborators.add(new_collaborator)

        return JsonResponse({"message": "user added successfully"}, status=200)
    
    except Exception as e:
        return JsonResponse({"message": str(e)})

def search_collaborators_api(request, substring):

    try:
        matched = User.objects.filter(Q(username__startswith=substring))

        serializer = UserSerializer(matched, many=True)

        return JsonResponse({"message":"request successful", "users": serializer.data}, status=200)
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=500)



@login_required
def remove_collaborator_api(request, repositorypk):
    raw_content = request.body
    loaded_content = json.loads(raw_content)
    collaboratorpk = loaded_content.get("pk")

    try:
        repository = Directory.objects.get(pk= repositorypk)
        collaborator = User.objects.get(pk=collaboratorpk)

        repository.collaborators.remove(collaborator)

        return JsonResponse({"message": f"{collaborator.username} removed successfully"}, status=200)
    except Directory.DoesNotExist:
        return JsonResponse({"message": f"repository with id {repositorypk} can't be found."}, status=400)
    except User.DoesNotExist: 
        return JsonResponse({"message": f"user with id {collaboratorpk} can't be found"}, status=401)
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=500)

def notifications_api(request):
    notifications = request.user.notifications
    serializer = NotificationSerializer(notifications, many=True)
    return JsonResponse({"notifications": serializer.data})

def directory_api(request, pk: int):
    try:
        directory = Directory.objects.get(pk=pk)
        directory_serializer = DirectorySerializer(directory)
        
        subdirectories = directory.subdirectories
        subdirectories_serializer = DirectorySerializer(subdirectories, many=True)

        files = directory.files
        file_serializer = FileSerializer(files, many=True)

        #add the parent directory if there is one, otherwise, set the parent field to null
        parent = directory.parent
        parent_serializer = DirectorySerializer(parent) if parent else None
        parent_data = parent_serializer.data if parent_serializer else None

        return JsonResponse({"parent": parent_data, "current": directory_serializer.data, "subdirectories":subdirectories_serializer.data, "files": file_serializer.data})

    except Directory.DoesNotExist:
        return JsonResponse({"message": f"directory with id {pk} does not exist"}, status=400)
    except FileModel.DoesNotExist:
        return JsonResponse({"message": f"file with id {pk} does not exist"}, status=400)
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=500)
    
def new_directory_api(request):
    #get name and parent pk
    raw_content = request.body
    loaded_content = json.loads(raw_content)
    name = loaded_content.get("name")
    parent_pk = loaded_content.get("parent_pk")

    try:
        #create new directory with parent
        parent= Directory.objects.get(pk=parent_pk)
        new_directory = Directory.objects.create(name= name, parent= parent, owner= parent.owner)
        new_directory.collaborators.set(parent.collaborators.all())
        new_directory.save()

        send_notifications(request.user, new_directory.repository, f"Directory {name} added by {request.user.username}")
        

        return JsonResponse({"message": "directory created successfully", "directory-pk": new_directory.pk}, status=200)
    except Directory.DoesNotExist:
        return JsonResponse({"message": f"directory with primary key {parent_pk} does not exist"}, status=400)
    except Exception as e:
        return JsonResponse({"message":f"{str(e)} \n user: {request.user.username}"}, status=500)
    
@login_required
def delete_directory_api(request):
    raw_content = request.body
    loaded_content = json.loads(raw_content)
    directorypk = loaded_content.get("directorypk")

    try:
        directory = Directory.objects.get(pk=directorypk)
        
        if not directory.is_repository:
            send_notifications(request.user, directory.repository, f"Directory  {directory.name} was deleted with its contents by {request.user.username}")

        directory.delete()

        return JsonResponse({"message": "directory deleted successfully"})
    except Directory.DoesNotExist:
        return JsonResponse({"message": f"primary key {directorypk} doesn't match any existing directory"}, status=400)
    except Exception as e:
        return JsonResponse({"message": f"delete api got Error: {str(e)}"}, status=500)

@login_required
def delete_file_api(request):
    raw_content = request.body
    loaded_content = json.loads(raw_content)
    filepk = loaded_content.get("filepk")

    try:
        file = FileModel.objects.get(pk=filepk)

        send_notifications(request.user, file.repository, f"File {file.filename} was deleted by {request.user.username}") 

        file.delete()
        return JsonResponse({"message": "file deleted successfully"})
    except FileModel.DoesNotExist:
        return JsonResponse({"message": f"primary key {filepk} doesn't match any existing directory"}, status=400)
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=500)

def upload_file_api(request):
    try:
        file = request.FILES.get('file')
        parentpk = request.POST.get('parentpk')
        parent = Directory.objects.get(pk=int(parentpk))
    
        file_instance = FileModel.objects.create(parent=parent, file=file)
        file_instance.save()

        send_notifications(request.user, file_instance.parent.repository, f"File {file_instance.filename} added by {request.user.username}")

        return JsonResponse({'message': 'File uploaded sucessfully'}, status=200)
    except Directory.DoesNotExist:
        return JsonResponse({'message': f'Parent directory with PRIMARY KEY: {parentpk} not found'}, status=400)
    except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)

@login_required
def new_comment(request):

    try:
        #retreive repository
        raw_content = request.body
        loaded_content = json.loads(raw_content)

        message = loaded_content.get("comment")
        repositorypk = loaded_content.get("repositorypk")

        repository = Directory.objects.get(pk=int(repositorypk))

        #create comment
        comment_instance = Comment.objects.create(comment=message, repository=repository, user=request.user)
        comment_instance.save()

        send_notifications(request.user, repository, f"{request.user.username} commented")

        return JsonResponse({'message': "comment saved successfully"})
    except Directory.DoesNotExist:
        return JsonResponse({'message': f'directory with PRIMARY KEY: {repositorypk} not found'}, status=400)
    except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)

def get_comments_api(request, repositorypk):
    repository = Directory.objects.get(pk=repositorypk)
    comments = repository.comments.order_by("-timestamp")
    comments_serializer = CommentSerializer(comments, many=True)

    return JsonResponse({"comments": comments_serializer.data})
