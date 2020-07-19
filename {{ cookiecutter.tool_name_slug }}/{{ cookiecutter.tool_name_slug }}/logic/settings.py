import configparser
from dataclasses import dataclass

@dataclass
class Settings:
    last_action: str = None

    def setParsedOptions(self, parser, issues):
        if parser.has_section('actions'):
            self.last_action = parser.get('actions','last_action', self.last_action)

    def copySettingsToParser(self, parser):
        parser.add_section('actions')
        if self.last_action:
            parser.set('actions', 'last_action', self.last_action)

