from typing import List, Dict
from pydantic import BaseModel
from src.definition.model import ChangeEvent
from src.definition.graph import MetricLineageGraph

class ImpactReport(BaseModel):
    event_id: str
    impacted_metrics: List[str]
    # Simple score based on depth or number of dependents
    severity_score: int 

class ImpactAnalyzer:
    def __init__(self, lineage_graph: MetricLineageGraph):
        self.graph = lineage_graph

    def analyze(self, event: ChangeEvent) -> ImpactReport:
        impacted_set = set()
        
        # 1. Direct impacts
        for metric in event.related_metrics:
            if metric in self.graph.metrics:
                impacted_set.add(metric)
                
                # 2. Downstream impacts (Structural)
                downstream = self.graph.get_downstream_impact(metric)
                impacted_set.update(downstream)
        
        # Calculate severity (simple count for now)
        score = len(impacted_set)
        
        return ImpactReport(
            event_id=event.id,
            impacted_metrics=list(impacted_set),
            severity_score=score
        )
