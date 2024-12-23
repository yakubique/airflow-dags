from pathlib import Path

import kfp
from kfp.compiler import Compiler
from pipelines.shikimori_etl import shikimori_etl_pipeline
from pipelines.test import test_pipeline

base_dir = Path.cwd()
output_dir = base_dir / "compiled"

# Compile the pipeline to YAML
Compiler().compile(test_pipeline, str(output_dir / "test.yaml"))
Compiler().compile(shikimori_etl_pipeline, str(output_dir / "shikimori_etl.yaml"))

# Upload and run the pipeline from Python code
client = kfp.Client(
    host="https://kubeflow.local.opa-oz.live"
)  # Connects to the KFP instance
client.create_run_from_pipeline_package(str(output_dir / "shikimori_etl.yaml"))
