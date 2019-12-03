import os
import requests


class CreateGitignore:
    def __init__(self, new_file: str = None, start_file: str = None, urls: list = None):
        if urls is None:
            self.urls = ["https://raw.githubusercontent.com/github/gitignore/master/Python.gitignore",
                         "https://raw.githubusercontent.com/github/gitignore/master/community/Python/JupyterNotebooks.gitignore",
                         "https://raw.githubusercontent.com/github/gitignore/master/Global/JetBrains.gitignore"]
        else:
            self.urls = urls

        self.start_file = start_file
        self.new_file = new_file
        self.git_file = ""

    def create(self):
        self.git_file += self.open_file()

        for u in self.urls:
            self.git_file += self.get_github_file(u)

    def open_file(self):
        try:
            with open(self.start_file, 'r') as file:
                return file.read()
        except Exception as e:
            print(e)
            return ""

    @staticmethod
    def get_github_file(url: str = None) -> str:
        if url is None:
            return ""

        r = requests.get(url)
        if r.status_code == 200:
            return r.text

        return ""

    def write_file(self):
        try:
            with open(self.new_file, 'w') as file:
                file.write(self.git_file)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    s_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", 'start_files', "gitignore.txt")
    n_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", 'test_files', "new.gitignore")
    cg = CreateGitignore(new_file=n_file, start_file=s_file)
    cg.create()
    cg.write_file()
