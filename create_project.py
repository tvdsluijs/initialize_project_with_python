#!/usr/bin/env python

import os
import sys
import configparser
import traceback

from pathlib import Path
from github import Github

from functions.create_gitignore import CreateGitignore
from functions.create_readme import CreateReadme

class CreateProject:
    def __init__(self):
        try:
            self.gitignore_start_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'start_files', "gitignore.txt")
            self.readme_start_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'start_files', "readme.txt")
            self.dir_path = os.path.dirname(os.path.realpath(__file__))
            self.config_file = os.path.join(self.dir_path, './config.ini')
            self.config = None
            self.read_config()

            try:
                home_folder = str(Path.home())  # this is the users home folder on any OS
                self.prod_fol = self.config['projects']['folder_name']
                self.project_folder = os.path.join(home_folder, self.prod_fol)
            except KeyError as e:
                raise Exception(f"Config file broken {e}")

            self.yn = ['y', 'n']
            self.checkers = [None, ""]
            self.correct = 1
            self.repo = None
            self.user = None
            self.project_name = None
            self.private_repo = None
            self.auto_init = None
            self.description = None
            self.homepage = None
            self.venv = False
        except Exception as e:
            print(f"We have an error: {e}")
            print(traceback.format_exc())
            sys.exit()


    def checkup(self):
        try:
            if self.config['github']['token'] is None or self.config['github']['token'] == '':
                raise Exception("No GitHub Token")
            if not os.path.exists(self.project_folder):
                raise Exception(f"Sorry, but your projects folder does not exists! {self.project_folder}")
        except KeyError as e:
            print(f"We have an error: {e}")
            print(traceback.format_exc())
            sys.exit()
        except Exception as e:
            print(f"We have an error: {e}")
            print(traceback.format_exc())
            sys.exit()

    def questionaire(self):
        self.get_project_name()
        self.what_repo()
        self.create_readme_init()
        self.get_description()
        self.get_homepage_url()
        self.get_create_venv()

    def get_create_venv(self):
        while self.venv not in self.yn:
            self.venv = input(f"Do you want to create a .venv (virtual environment) for this python project? {str(self.yn)} : ")
            if self.venv == "y":
                self.venv = True
                break
            elif self.venv == "n":
                self.venv = False
                break

    def get_project_name(self):
        while self.project_name in self.checkers:
            self.project_name = input("What is the name of your new project? ")
            while self.correct not in self.yn and self.project_name not in self.checkers:
                self.correct = input(f"Is this project name correct? {self.project_name} - {str(self.yn)} : ")
                if self.correct == "y":
                    break

    def what_repo(self):
        while self.private_repo not in self.yn:
            self.private_repo = input(f"Do you want to create a private repository? 'n'/No will create a public repo. {str(self.yn)} : ")
            if self.private_repo == "y":
                self.private_repo = True
                break
            elif self.private_repo == "n":
                self.private_repo = False
                break

    def create_readme_init(self):
        while self.auto_init in self.checkers:
            self.auto_init = input(f"Do you want to create a readme file and initialize the repository? {str(self.yn)} : ")
            if self.auto_init == "y":
                self.auto_init = True
                break
            elif self.auto_init == "n":
                self.auto_init = False
                break

    def get_description(self):
        while self.description in self.checkers:
            self.description = input("Please provide a small repository description. (you can change it later) ")

    def get_homepage_url(self):
        while self.homepage in self.checkers:
            self.homepage = input("Please proivde a url with more information about your repository. "
                                    "(you can change it later) ")

    def read_config(self):
        if not os.path.isfile(self.config_file):
            print('There is no config.ini file!')
            sys.exit()

        self.config = configparser.ConfigParser()
        self.config.read(self.config_file)

    def create_extra_files(self):
        new_file = os.path.join(self.project_folder, self.repo.name, ".gitignore")
        cg = CreateGitignore(new_file=new_file, start_file=self.gitignore_start_file)
        cg.create()
        cg.write_file()

        my_new_file = os.path.join(self.project_folder, self.repo.name, "README.md")
        cr = CreateReadme(project_name=self.project_name, descr=self.description,
                          github_username=self.repo.owner.login,
                          repo=self.repo.name,
                          readme_file= my_new_file,
                          example_readme=self.readme_start_file,
                          twitter=self.config['social']['twitter'],
                          email=self.config['social']['email'])
        cr.gogo_gadget()

    def create_git_repository(self):
        try:
            self.user = Github(self.config['github']['token']).get_user()

            self.repo = self.user.create_repo(
                self.project_name,
                auto_init=self.auto_init,
                homepage=self.homepage,
                description=self.description,
                private=self.private_repo,
                license_template=self.config['license']['template']
            )

            return True
        except Exception as e:
            print(f"We have an error: {e}")
            print(traceback.format_exc())
            sys.exit()

    def clone_git_repository(self):
        try:
            if self.repo.ssh_url is None:
                raise Exception("There is no GitHub ssh repository URL!")

            # unfortunately there is no way (yet) to clone with pygithub
            clone = f"git clone {self.repo.ssh_url}"
            os.chdir(self.project_folder)  # Specifying the path where the cloned project needs to be copied
            os.system(clone)  # Cloning
            return True

        except Exception as e:
            print(f"We have an error: {e}")
            print(traceback.format_exc())
            sys.exit()

    def create_venv(self):
        try:
            if self.venv:
                venv_me = "python -m venv .venv"
                os.chdir(os.path.join(self.project_folder, self.repo.name))
                os.system(venv_me)  # Cloning

        except Exception as e:
            print(f"We have an error: {e}")
            sys.exit()


if __name__ == "__main__":
    c = CreateProject()
    c.checkup()
    c.questionaire()
    c.create_git_repository()
    c.clone_git_repository()
    c.create_extra_files()
    c.create_venv()
