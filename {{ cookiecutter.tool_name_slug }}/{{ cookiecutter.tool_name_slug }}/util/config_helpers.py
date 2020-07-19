from pathlib import Path

def asPath(input: str) -> Path:
	"""This can be used to extend ConfigParser to understand Path types."""
    return Path(input)

