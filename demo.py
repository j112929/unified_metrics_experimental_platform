import sys
import os
import random
import time

# Ensure src is in path
sys.path.append(os.getcwd())

from src.definition.loader import load_from_yaml
from src.definition.graph import MetricLineageGraph
from src.definition.model import ChangeEvent, ChangeType
from src.rca_engine.impact_analysis import ImpactAnalyzer
from src.alert_engine.anomaly import ZScoreDetector

def title(text):
    print(f"\n{'='*50}\n{text}\n{'='*50}")

def main():
    title("Unified Metrics & Experimentation Platform - Demo")

    # 1. Load Metrics & Build Lineage
    metrics = load_from_yaml("examples/metrics.yaml")
    print(f"Loaded {len(metrics)} metrics from YAML.")
    
    graph = MetricLineageGraph()
    graph.load_metrics(metrics)
    graph.validate()
    print("Lineage Graph built and validated.")
    
    # 2. Show Lineage
    title("1. Metric Lineage (Root Cause & Impact)")
    target = "ad_impressions"
    upstream = graph.get_upstream_lineage(target)
    downstream = graph.get_downstream_impact(target)
    print(f"Metric: {target}")
    print(f"  <- Depends on: {upstream}")
    print(f"  -> Impacts:    {downstream}")

    # 3. Impact Analysis
    title("2. Change Impact Analysis")
    # Simulate a deployment that touches 'ad_clicks' logic
    event = ChangeEvent(
        id="deploy-001",
        type=ChangeType.DEPLOYMENT,
        timestamp=time.time(),
        service="ad-service",
        description="Fix click tracking logic",
        related_metrics=["ad_clicks"]
    )
    print(f"Event: {event.description} (affects 'ad_clicks')")
    
    analyzer = ImpactAnalyzer(graph)
    report = analyzer.analyze(event)
    
    print(f"Impact Report (Score: {report.severity_score}):")
    for m in report.impacted_metrics:
        print(f"  [WARN] Metric '{m}' may be unstable.")

    # 4. Anomaly Detection
    title("3. Automated Anomaly Detection")
    detector = ZScoreDetector(threshold=2.0)
    
    # Generate normal traffic (mean=100, std=10)
    history = [random.gauss(100, 10) for _ in range(50)]
    detector.fit(history)
    print("Detector trained on 50 normal data points (N(100, 10)).")
    
    # Test cases
    test_values = [105, 98, 110, 150, 85] # 150 should be anomaly
    
    print(f"{'Value':<10} | {'Anomaly?':<10} | {'Score':<10} | {'Range'}")
    print("-" * 50)
    for v in test_values:
        res = detector.predict(v)
        anom_str = "YES" if res.is_anomaly else "No"
        range_str = f"[{res.expected_range[0]:.1f}, {res.expected_range[1]:.1f}]"
        print(f"{v:<10.1f} | {anom_str:<10} | {res.score:<10.2f} | {range_str}")

if __name__ == "__main__":
    main()
