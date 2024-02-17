from .default import Settings

settings = None

__all__ = ['settings']

def initialize():
    global settings
    settings = Settings()

initialize()