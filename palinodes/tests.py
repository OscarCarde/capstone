from django.test import TestCase
from .models import *

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