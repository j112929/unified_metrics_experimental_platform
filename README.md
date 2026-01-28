# Unified Metrics & Experimentation Platform

A staff-level unified platform for metrics definition, streaming aggregation, querying, alerting, and root cause analysis (RCA).

## Core Architecture

The platform follows a standard data engineering lifecycle with advanced capabilities for governance and intelligence:

`Metrics Definition` → `Streaming Aggregation` → `Query Layer` → `Alerting` → `Root Cause Analysis`

## Key Focus Areas

1.  **Metrics Lineage**: Automated extraction of dependencies between raw events, intermediate tables, and final metrics.
2.  **Change Impact Analysis**: Correlating infrastructure/code changes with metric deviations.
3.  **Automated Anomaly Detection**: Unsupervised learning models to detect metric anomalies without manual thresholding.

## Architecture Guidelines

*   **Definition as Code**: All metrics are defined in version-controlled YAML/DSL.
*   **Stream-First**: Metrics are aggregated in real-time.
*   **Metadata Driven**: Lineage and Impact Analysis rely on a centralized metadata store.

## Tech Stack (MVP)

*   **Language**: Python 3.10+
*   **Processing**: In-memory streaming (simulating Flink/Spark)
*   **Storage**: Time-series optimized (simulating ClickHouse/Druid)
*   **Analysis**: Pandas/Scikit-learn for RCA and Anomaly Detection

## Running the Demo

1.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
2.  Run the MVP demonstration:
    ```bash
    python3 demo.py
    ```
    This script demonstrates:
    *   Loading metrics from `examples/metrics.yaml`.
    *   Building and querying the Lineage Graph.
    *   Simulating a Change Event and calculating Impact.
    *   Training an Anomaly Detector and flagging outliers.

3.  **Run the Web Dashboard**:
    ```bash
    python3 run_server.py
    ```
    Open [http://localhost:8000](http://localhost:8000) to view:
    *   **Interactive Lineage Graph**: Drag and drop nodes to see relationships.
    *   **Impact Simulator**: Choose a metric to "break" and see downstream effects.
    *   **Anomaly Checker**: Test values against the statistical model.


