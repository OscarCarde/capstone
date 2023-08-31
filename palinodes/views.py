from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
import json

from django.db import IntegrityError

from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import User, Profile, Directory, FileModel, Comment
from .forms import RepositoryForm
from .serializers import DirectorySerializer, FileSerializer, CommentSerializer

#################__LANDING__########################

def index(request):
    return HttpResponseRedirect('dashboard')

@login_required
def dashboard(request):
     return render(request, "palinodes/dashboard.html")

class CreateRepository(LoginRequiredMixin, CreateView):
    model = Directory
    form_class = RepositoryForm
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        # Use reverse to generate the URL using the model's id
        return reverse("repository", args=[str(self.object.id)])



def repository_view(request, repository_id):
    repository = Directory.objects.get(id=repository_id)
    return render(request, "palinodes/repository.html", {
        "repository": repository
    })

##################__APIS__##########################
@login_required
def directory_api(request, pk):
    try:
        directory = Directory.objects.get(pk=pk)
        directory_serializer = DirectorySerializer(directory)
        
        subdirectories = directory.subdirectories
        subdirectories_serializer = DirectorySerializer(subdirectories, many=True)

        files = directory.files
        print(files.values())
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
@login_required
def new_directory_api(request):
    
    #get name and parent pk
    raw_content = request.body
    loaded_content = json.loads(raw_content)
    name = loaded_content.get("name")
    parent_pk = loaded_content.get("parent_pk")

    #create new directory with parent
    parent= Directory.objects.get(pk=parent_pk)
    new_directory = Directory.objects.create(name= name, parent= parent, owner= parent.owner)
    new_directory.collaborators.set(parent.collaborators.all())
    new_directory.save()

    return JsonResponse({"directory-pk": new_directory.pk})

@login_required
def delete_directory_api(request):
    raw_content = request.body
    loaded_content = json.loads(raw_content)
    directorypk = loaded_content.get("directorypk")

    try:
        directory = Directory.objects.get(pk=directorypk)
        directory.delete()
        return JsonResponse({"message": "directory deleted successfully"})
    except Directory.DoesNotExist:
        return JsonResponse({"message": f"primary key {directorypk} doesn't match any existing directory"}, status=400)
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=500)

@login_required
def delete_file_api(request):
    raw_content = request.body
    loaded_content = json.loads(raw_content)
    filepk = loaded_content.get("filepk")

    try:
        file = FileModel.objects.get(pk=filepk)
        file.delete()
        return JsonResponse({"message": "file deleted successfully"})
    except FileModel.DoesNotExist:
        return JsonResponse({"message": f"primary key {filepk} doesn't match any existing directory"}, status=400)
    except Exception as e:
        print(e)
        return JsonResponse({"message": str(e)}, status=500)

@login_required
def upload_file_api(request):
    try:
        file = request.FILES.get('file')
        parentpk = request.POST.get('parentpk')
        print("parentpk: ", parentpk)
        parent = Directory.objects.get(pk=int(parentpk))
    
        file_instance = FileModel.objects.create(parent=parent, file=file)
        file_instance.save()
        return JsonResponse({'message': 'File uploaded sucessfully'})
    except Directory.DoesNotExist:
        return JsonResponse({'message': f'Parent directory with PRIMARY KEY: {parentpk} not found'}, status=400)
    except Exception as e:
        print(e)
        return JsonResponse({'message': str(e)}, status=500)

@login_required
def new_comment(request):

    try:
        raw_content = request.body
        loaded_content = json.loads(raw_content)

        message = loaded_content.get("comment")
        repositorypk = loaded_content.get("repositorypk")

        repository = Directory.objects.get(pk=int(repositorypk))

        comment_instance = Comment.objects.create(comment=message, repository=repository, user=request.user)
        comment_instance.save()

        return JsonResponse({'message': "comment saved successfully"})
    except Directory.DoesNotExist:
        return JsonResponse({'message': f'directory with PRIMARY KEY: {repositorypk} not found'}, status=400)
    except Exception as e:
        print(e)
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
