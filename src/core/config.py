# src/aiswarm/core/config.py
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class AgentConfig(BaseModel):
    name: str
    image: Optional[str]
    build_path: Optional[Path]
    replicas: int = 1
    resources: Dict[str, str] = Field(default_factory=dict)

class SwarmConfig(BaseModel):
    project_name: str
    version: str
    registry: Optional[str]
    provider: str = "aws"
    agents: List[AgentConfig]