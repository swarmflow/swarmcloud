# src/aiswarm/utils/errors.py
class SwarmError(Exception):
    """Base exception for all swarm errors"""
    pass

class ProjectInitError(SwarmError):
    """Raised when project initialization fails"""
    pass

class ProjectExistsError(SwarmError):
    """Raised when trying to create a project in a location that already contains a swarm project"""
    pass