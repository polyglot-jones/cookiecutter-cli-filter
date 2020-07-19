import configparser, shutil, os
from pathlib import Path

from dataclasses import dataclass
import app.logic.settings as sett_logic

from exceptions import {{ cookiecutter.tool_name_camel_case }}ConfigError, EnvironmentWarning
import ..util.config_helpers 

LOG = logging.getLogger("{{ cookiecutter.tool_name }}")


@dataclass
class Settings:
	"""
	"Settings" get written back to storage (vs."configs" that are read-only).
	Settings includes things like the last size and placement of a window, and the MRU file list.

	The logic subfolder has its own (child) Settings object. 
	Be sure to follow that pattern when adding additional subfolders.
	"""
	logic: sett_logic.Settings

	def __init__(self):
		self.logic = sett_logic.Settings()

	def setParsedOptions(self, parser, issues):
		""'Load the core settings from storage."""
		if parser.has_section('some_section'):
			self.upper_limit = parser['some_section'].getint('upper_limit', self.upper_limit)

	def copySettingsToParser(self, parser):
		""'Write the core settings to storage."""
		parser.add_section('some_section')
		if self.upper_limit:
			parser.set('some_section', 'upper_limit', self.upper_limit)


	def setFromINIFile(self, settingsFilename: str):
		filepath = Path(settingsFilename)
		if filepath.exists():
			try:
				settingsFile = filepath.open(mode = "r")
			except Exception as e:
				raise {{ cookiecutter.tool_name_camel_case }}ConfigError(
					"Cannot read Settings file {0}. {1}".format(settingsFilename, e))
			ini = settingsFile.read()
			settingsFile.close()
			self.setFromINIContents(ini)

	def saveToINIFile(self, settingsFilename: str):
		try:
			settingsFile = open(settingsFilename, "wt")
		except Exception as e:
			raise {{ cookiecutter.tool_name_camel_case }}ConfigError(
				"Cannot write Settings file {0}. {1}".format(settingsFilename, e))

		parser = configparser.ConfigParser()
		self.core.copySettingsToParser(parser)
		self.logic.copySettingsToParser(parser)
		parser.write(settingsFile)

	def setFromINIContents(self, settingsFilecontents: str):
		ADDITIONAL_CONFIGPARSER_CONVERTERS = {
			'path': util.config_helpers.asPath
		}
		parser = configparser.ConfigParser(
			converters=ADDITIONAL_CONFIGPARSER_CONVERTERS)
		parser.read_string(settingsFilecontents)
		issues = []

		self.core.setParsedOptions(parser, issues)
		self.logic.setParsedOptions(parser, issues)

		if issues:
			raise {{ cookiecutter.tool_name_camel_case }}ConfigError("\n".join(issues))

