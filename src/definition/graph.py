import networkx as nx
from typing import Dict, List, Set, Any
from .model import MetricDefinition

class MetricLineageGraph:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.metrics: Dict[str, MetricDefinition] = {}

    def add_metric(self, metric: MetricDefinition):
        self.metrics[metric.name] = metric
        self.graph.add_node(metric.name, type=metric.type, owner=metric.owner)
        
        for dep in metric.dependencies:
            # Direction: Dependency -> Dependent Metric
            # Allows traversing upstream (roots) and downstream (impact)
            self.graph.add_edge(dep, metric.name)

    def load_metrics(self, metrics: List[MetricDefinition]):
        for m in metrics:
            self.add_metric(m)

    def get_upstream_lineage(self, metric_name: str) -> List[str]:
        """Find root causes (ancestors)"""
        if metric_name not in self.graph:
            return []
        return list(nx.ancestors(self.graph, metric_name))

    def get_downstream_impact(self, metric_name: str) -> List[str]:
        """Find impacted metrics (descendants)"""
        if metric_name not in self.graph:
            return []
        return list(nx.descendants(self.graph, metric_name))

    def validate(self):
        """Check for cycles and missing dependencies"""
        if not nx.is_directed_acyclic_graph(self.graph):
            raise ValueError("Cycle detected in metric lineage!")
        
        for node in self.graph.nodes():
            for dep in self.metrics[node].dependencies:
                if dep not in self.metrics:
                    raise ValueError(f"Metric '{node}' depends on unknown metric '{dep}'")

    def export_graph(self) -> Dict[str, Any]:
        return nx.node_link_data(self.graph)
