from gwpycore import GruntWurkError

class {{ cookiecutter.tool_name_camel_case }}Error(GruntWurkError):
    pass


__all__ = ("{{ cookiecutter.tool_name_camel_case }}Error",)
