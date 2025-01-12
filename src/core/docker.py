# src/aiswarm/core/docker.py
import docker
from typing import Optional
from pathlib import Path

class DockerManager:
    def __init__(self):
        self.client = docker.from_env()
    
    def build_image(
        self,
        path: Path,
        tag: str,
        dockerfile: Optional[Path] = None
    ):
        """Build a Docker image"""
        self.client.images.build(
            path=str(path),
            tag=tag,
            dockerfile=str(dockerfile) if dockerfile else None
        )