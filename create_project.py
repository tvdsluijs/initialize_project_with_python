import os
import sys
import logging
from datetime import datetime
from pathlib import Path

from github import Github
from functions.readConfig import readConfig

if __name__ == '__main__':
    log_format = "%(asctime)s [%(levelname)8s] --- %(filename)10s :: %(lineno)3d :: %(message)s"
    logger = logging.getLogger("DEBUG LOGGER")

    # To override the default severity of logging
    logger.setLevel('DEBUG')

    # Use FileHandler() to log to a file
    file_handler = logging.StreamHandler()
    formatter = logging.Formatter(log_format, "%Y-%m-%d %H:%M:%S")
    file_handler.setFormatter(formatter)

    # Don't forget to add the file handler
    logger.addHandler(file_handler)
else:
    logger = logging.getLogger("DEBUG LOGGER")


class Create:
    def __init__(self):
        try:
            config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config', 'config.yml')
            cf = readConfig(config_file)
            try:
                self.GitHub_Token = cf.config['github_token']
                self.projects_folder_name = cf.config['projects_folder_name']
                self.license_template = cf.config['license_template']
            except KeyError as e:
                raise Exception(f"Config file broken {e}")

            yn = ['y', 'n']
            checkers = [None, ""]
            correct = 1
            self.repo = None

            if self.GitHub_Token is None or self.GitHub_Token == '':
                raise Exception("No GitHub Token")

            home_folder = str(Path.home())  # this is the users home folder on any OS
            self.project_folder = os.path.join(home_folder, self.projects_folder_name)

            project_folder = Path(self.project_folder)
            if not project_folder.exists():
                raise Exception("Sorry, but your projects folder does not exists! {} ".format(self.project_folder))

            self.project_name = None
            while self.project_name in checkers:
                self.project_name = input("What is the name of your new project? ")
                while correct not in yn and self.project_name not in checkers:
                    correct = input("Is this project name correct? {} - {} : ".format(self.project_name, str(yn)))
                    if correct == "y":
                        break

            self.private_repo = None
            while self.private_repo not in yn:
                self.private_repo = input("Do you want to create a public repository? {} : ".format(str(yn)))
                if self.private_repo == "y":
                    self.private_repo = True
                    break
                elif self.private_repo == "n":
                    self.private_repo = False
                    break

            self.auto_init = None
            while self.auto_init in checkers:
                self.auto_init = input("Do you want to create a readme file and initialize the repository? {} : "
                                       "".format(str(yn)))
                if self.auto_init == "y":
                    self.auto_init = True
                    break
                elif self.auto_init == "n":
                    self.auto_init = False
                    break

            self.description = None
            while self.description in checkers:
                self.description = input("Please provide a small repository description. (you can change it later) ")

            self.homepage = None
            while self.homepage in checkers:
                self.homepage = input("Please proivde a url with more information about your repository. "
                                      "(you can change it later) ")

            if self.create_git_repository():
                self.clone_git_repository()

        except Exception as e:
            logger.warning(e)
            return

    def create_git_repository(self):
        try:
            user = Github(self.GitHub_Token).get_user()

            self.repo = user.create_repo(
                self.project_name,
                auto_init=self.auto_init,
                homepage=self.homepage,
                description=self.description,
                private=self.private_repo,
                license_template=self.license_template
            )

            return True
        except Exception as e:
            logger.warning(e)
            return False

    def clone_git_repository(self):
        try:
            if self.repo.ssh_url is None:
                raise Exception("There is no GitHub ssh repository URL!")

            # unfortunately there is no way (yet) to clone with pygithub
            clone = "git clone {}".format(self.repo.ssh_url)
            os.chdir(self.project_folder)  # Specifying the path where the cloned project needs to be copied
            os.system(clone)  # Cloning

        except Exception as e:
            logger.warning(e)


if __name__ == "__main__":
    c = Create()
