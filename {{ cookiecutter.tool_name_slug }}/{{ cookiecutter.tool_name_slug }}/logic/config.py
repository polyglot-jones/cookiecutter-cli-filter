from dataclasses import dataclass

@dataclass
class Configuration:
	data_folder: pathlib.Path = pathlib.Path("/local")

	def setParsedOptions(self, parser, issues):
		if parser.has_section('locations'):
			self.data_folder = parser['locations'].getPath('data_folder', self.data_folder)

	def runtimeValidation(self,issues):
		"""Look for non-passive problems in a running environment."""
		pass
