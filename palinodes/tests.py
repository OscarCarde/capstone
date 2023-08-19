from django.test import TestCase
from .models import *
from .serializers import *

from django.core.files import File

class DirectoryTestCase(TestCase):

    def setUp(self):
        self.user1 = User.objects.create(id=1000, username = "Alice")
        self.repo = Repository.objects.create(name="repo", owner = self.user1)
        self.dir1 = Directory.objects.create(name = "dir1", parent = self.repo)
        self.dir2 = Directory.objects.create(name = "dir11", parent=self.dir1)
        self.dir3 = Directory.objects.create(name = "dir111", parent=self.dir2)

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
        self.repo = Repository.objects.create(name="test_repository", owner = self.user)
        self.dir = Directory.objects.create(name = "test_directory", parent = self.repo)
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
        self.repo = Repository.objects.create(id=1000, name="repo", description=self.description, owner = self.user1)
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
    
