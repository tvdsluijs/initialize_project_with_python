## Initialize a project with Python
Small python script to automate the creation of a project in GitHub and your harddrive.

[![Project Automator](https://img.shields.io/badge/Project_Automator-version_0.9-green.svg)]()

## Installation
```bash
git clone git@github.com:tvdsluijs/initialize_project_with_python.git
cd initialize_project_with_python
pip install -r requirements.txt
source ~/.my_commands.sh
```

Create a Github [token](https://help.github.com/en/articles/creating-a-personal-access-token-for-the-command-line) 

Then go to the folder config and set the 3 variables in a `config.yml` file
- github_token              = Your Github token
- projects_folder_name      = where your projects folder is
- license_template          = Pick a for you appropriate license

Done!

## Why did I build this
Well you can read all about it in my blogpost.

## Build status
Build status is ready! 

[![Build Status](https://img.shields.io/badge/Build-Ready-Green.svg)]()


## Tech/framework used
[![Python](https://img.shields.io/badge/Python-3.5%20%7C%203.6%20%7C%203.7-blue.svg)]()

<b>Built with</b>

[![PyCharm](https://img.shields.io/badge/PyCharm-2018.3-blue.svg)]()

## This project Uses

- PyGithub
- pathlib
- PyYAML

It's all in the requirements.txt so when you clone this repository and fire the following command all be good!

`pip install -r requirements.txt`


## Help

Are you in need of help? Open slack and go to:

https://pure-python.slack.com

You will find more about this project in:

[#Initialize Projects](https://pure-python.slack.com/messages/CKKFAGFCM)


## License
<a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/">Creative Commons Attribution-NonCommercial 4.0 International License</a>.

@[Theo van der Sluijs](mailto:theo@vandersluijs.nl)