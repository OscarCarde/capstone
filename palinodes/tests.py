from django.test import TestCase
from .models import *

from django.core.files import File

class DirectoryTestCase(TestCase):

    def setUp(self):
        self.user1 = User(username = "Alice")
        self.repo = Repository(name="repo", owner = self.user1)
        self.dir1 = Directory(name = "dir1", parent_repository = self.repo)
        self.dir2 = Directory(name = "dir11", parent_repository = self.repo, parent_folder=self.dir1)
        self.dir3 = Directory(name = "dir111", parent_repository = self.repo, parent_folder=self.dir2)

    def test_directory_path(self):

        path1 = self.dir1.path
        self.assertEquals(f"{self.repo.name}/dir1", path1)
        path2 = self.dir2.path
        self.assertEquals(f"{self.repo.name}/dir1/dir11", path2)
        path3 = self.dir3.path
        self.assertEquals(f"{self.repo.name}/dir1/dir11/dir111", path3)
    
class FileTestCase(TestCase):
    '''
        Text fixture for File model
    '''

    def setUp(self) -> None:
        self.user = User.objects.create(username="Phillip")
        self.repo = Repository.objects.create(name="test_repository", owner = self.user)
        self.dir = Directory.objects.create(name = "test_directory", parent_repository = self.repo)
        with open("palinodes/testFiles/cvt.docx", 'rb') as file:
            self.file1 = FileModel(parent_folder=self.dir, parent_repository=self.repo)
            self.file1.file.save('cvt.docx', File(file))

    def tearDown(self):
        self.file1.file.delete()
        super().tearDown()

    def test_filename(self):
        self.assertEqual("cvt.docx", self.file1.filename, "The names don't match")


    def test_correct_path(self):
        self.assertEqual("test_repository/test_directory/cvt.docx", self.file1.file.name, "The paths don't match")