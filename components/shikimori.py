from typing import List

from kfp import dsl


@dsl.component(
    base_image="python:3.11",
    packages_to_install=["requests==2.32.3", "jsonlines==4.0.0"],
)
def grab_boundaries(output_list_path: dsl.OutputPath("jsonl")):
    page_size = 50
    base_url = "https://shikimori.one"
    base_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "Api Test",
    }

    from dataclasses import dataclass, fields

    @dataclass
    class PoorAnime(object):
        id: int
        name: str
        russian: str
        image: dict
        url: str
        kind: str
        score: str
        status: str
        episodes: int
        episodes_aired: int
        aired_on: str
        released_on: str

        @classmethod
        def from_json(cls, data: dict):
            keys = [f.name for f in fields(cls)]

            return cls(**{k: data.get(k) for k in keys})

    import json

    import requests
    from requests.adapters import HTTPAdapter, Retry

    def json_get(url: str, headers: dict) -> str:
        # https://stackoverflow.com/a/35636367
        session = requests.Session()
        retries = Retry(
            total=5, backoff_factor=2, status_forcelist=[429, 500, 502, 503, 504]
        )
        session.mount("https://", HTTPAdapter(max_retries=retries))

        req = session.get(url, headers=headers)

        if req.status_code >= 200 and req.status_code < 400:
            try:
                j = req.json()
            except json.JSONDecodeError:
                print("Error decoding JSON", req.text)
                return None

            return json.dumps(j)

        return None

    start_url = f"{base_url}/api/animes?order=id&limit=1&page=0"
    end_url = f"{base_url}/api/animes?order=id_desc&limit=1&page=0"

    start_data = json_get(start_url, base_headers)
    end_data = json_get(end_url, base_headers)

    start_anime = PoorAnime.from_json(json.loads(start_data)[0])
    end_anime = PoorAnime.from_json(json.loads(end_data)[0])

    to_go = end_anime.id - start_anime.id
    pages = to_go // page_size + 1

    import jsonlines

    with jsonlines.open(output_list_path, "w") as writer:
        for i in range(pages):
            page_url = f"{base_url}/api/animes?order=id&limit={page_size}&page={i}"
            print("Getting page", i, "of", pages)

            page_data = json_get(page_url, base_headers)
            page_json = json.loads(page_data)

            for anime in page_json:
                writer.write(anime)