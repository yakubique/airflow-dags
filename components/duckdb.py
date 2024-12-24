"""
Components that use the DuckDB library.
"""

from kfp import dsl  # pylint: disable=import-error


@dsl.component(base_image="python:3.11", packages_to_install=["duckdb==1.1.3"])
def jsonl_2_pq(
    json_input_path: dsl.InputPath("jsonl"), pq_output_path: dsl.OutputPath("parquet")
):
    """
    Converts a JSONL file to a Parquet file.
    """
    import duckdb  # pylint: disable=import-error,import-outside-toplevel

    duckdb.read_json(json_input_path)
    duckdb.sql(
        f"""
            SELECT *
            FROM read_ndjson_auto('{json_input_path}', format = 'newline_delimited')
        """
    ).write_parquet(pq_output_path)
