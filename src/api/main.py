from fastapi import FastAPI, HTTPException, Body
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Dict, Any
import networkx as nx
import random
import time

from src.definition.loader import load_from_yaml
from src.definition.graph import MetricLineageGraph
from src.rca_engine.impact_analysis import ImpactAnalyzer, ChangeEvent, ChangeType, ImpactReport

app = FastAPI(title="Unified Metrics Platform API")

# Global State
metrics = load_from_yaml("examples/metrics.yaml")
graph = MetricLineageGraph()
graph.load_metrics(metrics)
analyzer = ImpactAnalyzer(graph)

# --- Lineage ---

@app.get("/api/metrics")
def get_metrics():
    """Return all metric definitions."""
    return [m.dict() for m in metrics]

@app.get("/api/lineage")
def get_lineage_graph():
    """Return graph data in cytoscape/D3 compatible format"""
    d3_data = nx.node_link_data(graph.graph)
    # Enhance nodes with type info for visualization
    for node in d3_data['nodes']:
        m = graph.metrics.get(node['id'])
        if m:
            node['type'] = m.type
            node['owner'] = m.owner
    return d3_data

# --- Impact Analysis ---

class ImpactRequest(BaseModel):
    description: str
    related_metrics: List[str]

@app.post("/api/impact", response_model=ImpactReport)
def analyze_impact(request: ImpactRequest):
    """Simulate a change event and get impact report."""
    event = ChangeEvent(
        id=f"evt-{int(time.time())}",
        type=ChangeType.DEPLOYMENT,
        timestamp=time.time(),
        service="unknown",
        description=request.description,
        related_metrics=request.related_metrics
    )
    return analyzer.analyze(event)

# --- Anomaly Detection Simulation ---

class AnomalyCheck(BaseModel):
    metric: str
    value: float

class AnomalyResponse(BaseModel):
    is_anomaly: bool
    score: float
    expected_range: tuple

@app.post("/api/anomaly")
def check_anomaly(check: AnomalyCheck):
    """Simulate checking a value against a pre-trained detector."""
    # In a real app, we'd load the specific detector for the metric.
    # Here we simulate one.
    import random
    mean = 100
    std = 10
    threshold = 3.0
    
    z_score = (check.value - mean) / std
    is_anomaly = abs(z_score) > threshold
    
    return AnomalyResponse(
        is_anomaly=is_anomaly,
        score=z_score,
        expected_range=(mean - 3*std, mean + 3*std)
    )

# Static Files (Frontend)
app.mount("/", StaticFiles(directory="src/web", html=True), name="static")
