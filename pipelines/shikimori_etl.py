from components.print_files import print_json
from components.shikimori import grab_boundaries
from kfp import dsl


@dsl.pipeline
def shikimori_etl_pipeline():
    print_json(input_path=grab_boundaries().outputs["output_list_path"])
