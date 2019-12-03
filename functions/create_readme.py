import os
import re


class CreateReadme:
    def __init__(self, project_name: str = None, descr: str = None, github_username: str = None, repo: str = None,
                 readme_file: str = None, example_readme: str = None, twitter: str = None, email: str = None):
        self.title = project_name
        self.descr = descr
        self.repo = repo
        self.twitter = twitter
        self.github_username = github_username
        self.email = email
        self.readme_example = example_readme
        self.readme_file = readme_file
        self.readme = ""

    def gogo_gadget(self):
        self.readme = self.read_readme_example()
        self.readme = self.parse_readme_data()
        self.write_readme_project()

    def read_readme_example(self):
        try:
            with open(self.readme_example, 'r') as f:
                return f .read()
        except Exception as e:
            print(e)
            return ""

    def parse_readme_data(self):
        return self.multiple_replace(self.readme, {'twitter_handle': self.twitter,
                                                   'github_username': self.github_username,
                                                   'email': self.email, 'repo': self.repo,
                                                   'YOUR_SHORT_DESCRIPTION': self.descr,
                                                   'YOUR_TITLE': self.title})

    @staticmethod
    def multiple_replace(string, rep_dict):
        pattern = re.compile("|".join([re.escape(k) for k in sorted(rep_dict, key=len, reverse=True)]), flags=re.DOTALL)
        return pattern.sub(lambda x: rep_dict[x.group(0)], string)

    def write_readme_project(self):
        try:
            with open(self.readme_file, 'w') as f:
                f.write(self.readme)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    my_github_username = "tvdsluijs"
    my_email = "info@vandersluijs.nl"
    my_twitter = "tvdsluijs"
    my_repo = "my_extraordinary_project"
    my_name = 'My extraordinary project'
    my_start_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", 'start_files', "readme.txt")
    my_new_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", 'test_files', "readme.txt")
    my_descr = "Bla bla bla bla bla bla bla bla blaaaaahhhh !!!! Sheep!"
    cr = CreateReadme(project_name=my_name, descr=my_descr, github_username=my_github_username, repo=my_repo,
                      readme_file= my_new_file, example_readme=my_start_file, twitter=my_twitter, email=my_email)
    cr.gogo_gadget()
