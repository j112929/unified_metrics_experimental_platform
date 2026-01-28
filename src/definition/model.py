from typing import List, Optional, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field

class MetricType(str, Enum):
    COUNTER = "counter"
    GAUGE = "gauge"
    RATIO = "ratio"
    COMPOSITE = "composite"

class MetricDefinition(BaseModel):
    name: str
    description: Optional[str] = None
    type: MetricType
    owner: str
    
    # Primitive logic
    source_event: Optional[str] = None
    aggregation_field: Optional[str] = None
    
    # Derived logic
    expression: Optional[str] = None
    dependencies: List[str] = Field(default_factory=list)
    
    tags: Dict[str, str] = Field(default_factory=dict)

    class Config:
        frozen = True

class ChangeType(str, Enum):
    DEPLOYMENT = "deployment"
    CONFIG_UPDATE = "config"
    DATA_SCHEMA = "data_schema"

class ChangeEvent(BaseModel):
    id: str
    type: ChangeType
    timestamp: float
    service: str
    description: str
    # Which metrics might be DIRECTLY affected (e.g. config explicitly mentions them)
    # In a real system, we might infer this from the service map
    related_metrics: List[str] = Field(default_factory=list)

