import yaml
from typing import List
from .model import MetricDefinition

def load_from_yaml(path: str) -> List[MetricDefinition]:
    with open(path, 'r') as f:
        data = yaml.safe_load(f)
    
    metrics = []
    for m_data in data.get('metrics', []):
        metrics.append(MetricDefinition(**m_data))
    return metrics
