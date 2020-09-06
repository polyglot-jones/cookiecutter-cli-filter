# On Windows, make uses the shell specified by the SHELL environment variable if it exists (otherwise the ComSpec envvar)
# ?= means only assign if it doesn't already have a value
VENV_NAME?=.venv
BIN=$(VENV_NAME)\Scripts
LIB=${VENV_NAME}\Lib\site-packages
PYTHON=${VENV_NAME}\Scripts\python
NON_VIRTUAL_PYTHON?=${PY_HOME}\python
TEST_PATH=.\tests

.PHONY: help clean clean-pyc test examples activate linters requirements gwpycore dev-env format isort lint dist pip
.ONESHELL:

help: # If you just say `make`, then this first target is assumed as the goal
	@type doc_technical\makefile_help.txt

clean: clean-pyc # Deletes all temporary files
	del /Q /F /S build\
	del /Q /F /S dist\
	del /Q /F /S *.pyo
	del /Q /F /S *.egg-info

clean-pyc:
	del /Q /F /S *.pyc > nul

test: clean-pyc | .venv # Runs all of the unit tests
	${PYTHON} -m pytest --verbose --color=yes $(TEST_PATH)


.venv\pyvenv.cfg: # Installs a virtual environment for this project
	${NON_VIRTUAL_PYTHON} -m pip install --upgrade pip
	${NON_VIRTUAL_PYTHON} -m venv .venv

activate: | .venv\pyvenv.cfg # Force activate the virtual environment
		${BIN}\activate.bat

..\gwpycore\README.adoc: .venv # Clones the gwpycore source code and installs it (symlink-ish)
	git clone git@github.com:gruntwurk/gwpycore.git "..\gwpycore"

pip:
	${PYTHON} -m pip install --upgrade pip

gwpycore: ..\gwpycore\README.adoc
	${BIN}\pip install -e ..\gwpycore

qt-designer: # Install the QT-designer tool
	${NON_VIRTUAL_PYTHON} -m pip install pyqt5_tools

rcc:
	pyrcc5 .\{{ cookiecutter.tool_name_slug }}\gui\main_ui.qrc -o .\{{ cookiecutter.tool_name_slug }}\gui\main_ui_rc.py

linters:
	${BIN}\pip install black isort flake8

requirements:  # Ensures that all of the modules required by this project are installed (in the virtual env)
	${BIN}\pip install -r requirements.txt

dev-env: pip gwpycore requirements linters # Prepares the development environment -- use only once.

standardize: format isort lint # Apply of the linting tools to all of the .py files

format: # Re-formats all of the Python code (with black)
	${BIN}\black -l 256 .

isort: # Cleans up all of the imports (using isort)
	${BIN}\isort .

# Ignore these here, but not in .flake8...
# E301 expected 1 blank line, found 0
# F841 variable defined but never used
# E722 do not use bare 'except'
lint:   # Lints code (using flake8)
	${BIN}\flake8 --max-line-length=256 --extend-ignore=W191,W391,E203,E265,F841,E722,E301 --extend-exclude=.venv,.pytest_cache,.vscode,doc,doc_technical,*.egg-info . > lint_report.txt

dist:   #  Builds a distributable .EXE
	if exist .\dist\{{ cookiecutter.tool_name_slug }} rmdir /S /Q .\dist\{{ cookiecutter.tool_name_slug }}
	pyinstaller --clean --debug all --log-level=DEBUG {{ cookiecutter.tool_name_slug }}.spec 2> build.log
	touch .\dist\{{ cookiecutter.tool_name_slug }}\first_time_install.txt
	"C:\Program Files\7-Zip\7z.exe" a -sfx .\dist\{{ cookiecutter.tool_name_slug }}_sfx .\dist\*

