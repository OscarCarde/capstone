from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


from django.shortcuts import render, reverse
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
import json
from .helpers import send_notifications

from django.db import IntegrityError

from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import User, Profile, Directory, FileModel, Comment
from .forms import RepositoryForm, ProfileForm
from .serializers import DirectorySerializer, FileSerializer, CommentSerializer, NotificationSerializer

#################__LANDING__########################

def index(request):
    return HttpResponseRedirect('dashboard')

@login_required
def dashboard(request):
    if request.method == 'POST':
        print("WOLF FENCING: performing post method")
        profile = request.user.profile
        avatar = request.FILES.get("avatar")
        print("WOLF FENCING: checking file: \n" + str(request.FILES.keys()))
        description = request.POST.get("description")
        print("WOLF FENCING: checking description: \n" + description)
        if avatar:
            profile.avatar = avatar
        if description:
            profile.description = description

        profile.save() 
        
        return HttpResponseRedirect(reverse("dashboard"))

    return render(request, "palinodes/dashboard.html", {
        "profile_form": ProfileForm()
    })

class CreateRepository(LoginRequiredMixin, CreateView):
    model = Directory
    form_class = RepositoryForm
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        # Use reverse to generate the URL using the model's id
        return reverse("repository", args=[str(self.object.id)])


@login_required
def repository_view(request, repository_id):
    repository = Directory.objects.get(id=repository_id)

    #TODO refactor to avoid unnecessary exhaustive searches
    notifications = repository.notifications.all()
    for notification in notifications:
        if request.user in notification.recipients.all():
            notification.recipients.remove(request.user)
        if not notification.recipients.exists():
            notification.delete()

    allowed = request.user in repository.collaborators.all() or request.user == repository.owner

    if allowed:
        if request.method == 'POST':
            form = RepositoryForm(request.POST)
            if form.is_valid():
                try:
                    name = form.cleaned_data.get("name")
                    description = form.cleaned_data.get("description")
                    collaborators = form.cleaned_data.get("collaborators")

                    repository.name = name
                    repository.description = description

                    # Clear existing collaborators and add the selected ones
                    repository.collaborators.clear()
                    repository.collaborators.add(*collaborators)

                    repository.save()

                except Exception as e:
                    print(e)


        return render(request, "palinodes/repository.html", {
            "repository": repository, "repository_form": RepositoryForm()
        })
    else:
        return HttpResponseRedirect(reverse("dashboard"))

##################__APIS__##########################
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

##################__AUTHENTICATION__################
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "palinodes/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "palinodes/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "palinodes/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            profile = Profile.objects.create(user=user)
            profile.save()
        except IntegrityError:
            return render(request, "palinodes/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "palinodes/register.html")
