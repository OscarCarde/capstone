from django.test import Client, TestCase
from .models import *
from .serializers import *

from django.core.files import File

class DirectoryTestCase(TestCase):

    def setUp(self):
        self.user1 = User.objects.create(id=1000, username = "Alice")
        self.repo = Directory.objects.create(name="repo", owner = self.user1, description="a Test Repository")
        self.dir1 = Directory.objects.create(name = "dir1", owner = self.user1, parent = self.repo)
        self.dir2 = Directory.objects.create(name = "dir11", owner = self.user1, parent = self.dir1)
        self.dir3 = Directory.objects.create(name = "dir111", owner = self.user1, parent = self.dir2)

    def test_is_repository(self):
        self.assertEquals(True, self.repo.is_repository)

    def test_directory_path(self):
        path1 = self.dir1.path
        self.assertEquals(f"1000/{self.repo.name}/dir1", path1)
        path2 = self.dir2.path
        self.assertEquals(f"1000/{self.repo.name}/dir1/dir11", path2)
        path3 = self.dir3.path
        self.assertEquals(f"1000/{self.repo.name}/dir1/dir11/dir111", path3)
    
class FileTestCase(TestCase):
    '''
        Text fixture for File model
    '''

    def setUp(self) -> None:
        self.user = User.objects.create(id=1000, username="Phillip")
        self.repo = Directory.objects.create(name="test_repository", owner = self.user)
        self.dir = Directory.objects.create(name = "test_directory", owner = self.user, parent = self.repo)
        with open("palinodes/testFiles/cvt.docx", 'rb') as file:
            self.file1 = FileModel(parent=self.dir)
            self.file1.file.save('cvt.docx', File(file))

    def tearDown(self):
        self.file1.file.delete()
        super().tearDown()

    def test_filename(self):
        self.assertEqual("cvt.docx", self.file1.filename, "The names don't match")


    def test_correct_path(self):
        self.assertEqual("1000/test_repository/test_directory/cvt.docx", self.file1.file.name, "The paths don't match")

class RepositorySerializerTestCase(TestCase):
    def setUp(self) -> None:
        self.user1 = User.objects.create(id=1000, username = "Alice")
        self.user2 = User.objects.create(id=2000, username = "Bob")
        self.user3 = User.objects.create(id=3000, username = "Claire")
        self.description = "a test description for a test repository"
        self.repo = Directory.objects.create(id=1000, name="repo", description=self.description, owner = self.user1)
        self.repo.collaborators.add(self.user2)
        self.repo.collaborators.add(self.user3)
        self.serializer = RepositorySerializer(self.repo)

    def test_serializer_name(self):
        self.assertEquals('repo', self.serializer.data['name'], "repository names don't match")

    def test_serializer_description(self):
        self.assertEquals(self.description, self.serializer.data['description'], "repository description doesn't match")

    def test_serializer_owner(self):
        self.assertEquals('Alice', self.serializer.data['owner'], "repository owners don't match")

    def test_serializer_collaborators(self):
        self.assertListEqual(['Bob', 'Claire'], self.serializer.data["collaborators_names"], "The repository's collaborators' names don't match")
    
class ProfileTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(id=1000, username = "Alice")
        self.profile = Profile.objects.create(user=self.user, description="A test user profile")
        self.repo1 = Directory.objects.create(pk=1000, name="test repo1", owner = self.user, description="1 Test Repository")
        self.repo2 = Directory.objects.create(pk=2000, name="test repo2", owner = self.user, description="2 Test Repository")
        self.repo3 = Directory.objects.create(pk=3000, name="test repo3", owner = self.user, description="3 Test Repository")

    def test_repositories(self):
        actual_repositories = self.profile.repositories.values_list('pk', flat=True)
        self.assertListEqual([1000, 2000, 3000], list(actual_repositories), "the profile's repositories don't match")

        pk = 1000
        for repository in self.profile.repositories:
            self.assertEquals(pk, repository.pk, "repository doesn't match")
            pk += 1000

class DirectoryApiTestCase(TestCase):
    '''tests for the directory_api in views.py'''
    def setUp(self):
        self.user = User.objects.create(id=1000, username = "Alice")
        self.dir = Directory.objects.create(pk=2000, name="test dir", owner = self.user, description="Test Directory")
        self.dir1 = Directory.objects.create(pk=3000, name="test subdir", owner = self.user, parent=self.dir)
        with open("palinodes/testFiles/cvt.docx", 'rb') as file:
            self.file = FileModel(parent=self.dir)
            self.file.file.save('cvt.docx', File(file))

    def tearDown(self):
        self.file.file.delete()
        super().tearDown()

    def test_api_endpoint(self):
        c = Client()
        response = c.get(f"/directory/{self.dir.pk}")
        subdirectories = response.json()["subdirectories"]
        self.assertListEqual([{"pk":3000, "name":"test subdir"}], subdirectories, "subdirectories don't match")
        files = response.json()["files"]
        self.assertListEqual([{"filename": "cvt.docx", "fileurl": "/media/1000/test%20dir/cvt.docx"}], files, "files don't match")
        c.logout()
