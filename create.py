import os
import sys
import logging
from datetime import datetime
from pathlib import Path

from github import Github
from functions.readConfig import readConfig

# this part is for error logging purposes
now = datetime.now()
today = "{}-{}-{}".format(now.year, now.month, now.day)
sf = os.path.dirname(os.path.realpath(__file__))
folder = os.path.join(sf, 'logging')
log_file = os.path.join(folder, "{}.log".format(today))

os.makedirs(folder, exist_ok=True)
logging.basicConfig(filename=log_file, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)


class Create:
    def __init__(self):
        try:
            cf = readConfig("config/config.yml")

            self.GitHub_Token = cf.config['github_token']
            self.projects_folder_name = cf.config['projects_folder_name']
            self.license_template = cf.config['license_template']

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
            print(e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logging.warning(str(e) + " | " + str(exc_type) + " | " + str(f_name) + " | " + str(exc_tb.tb_lineno))
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
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logging.warning(str(e) + " | " + str(exc_type) + " | " + str(f_name) + " | " + str(exc_tb.tb_lineno))
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
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logging.warning(str(e) + " | " + str(exc_type) + " | " + str(f_name) + " | " + str(exc_tb.tb_lineno))
            return


if __name__ == "__main__":
    c = Create()
