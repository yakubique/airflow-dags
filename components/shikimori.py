"""
This component is responsible for grabbing the anime and manga data from the Shikimori API.
"""

from kfp import dsl  # pylint: disable=import-error


@dsl.component(
    base_image="python:3.11",
    packages_to_install=["requests==2.32.3", "jsonlines==4.0.0"],
)
def grab_pages(  # pylint: disable=too-many-statements,too-many-locals
    is_testing: bool,
    anime_path: dsl.OutputPath("jsonl"),
    manga_path: dsl.OutputPath("jsonl"),
):
    """
    Grabs the anime and manga pages from the Shikimori API.
    1. Grab the first and last anime/manga.
    2. Calculate the number of pages to grab.
    3. Grab the pages.
    4. Write the pages to a JSONL file.
    """
    page_size = 50
    base_url = "https://shikimori.one"
    base_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "Api Test",
    }

    from dataclasses import dataclass, fields  # pylint: disable=import-outside-toplevel

    @dataclass
    class PoorAnime:  # pylint: disable=too-few-public-methods,too-many-instance-attributes
        """
        Represents an anime object from the Shikimori API.
        """

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
            """
            Converts a JSON object to a `PoorAnime` object.
            """
            keys = [f.name for f in fields(cls)]

            return cls(**{k: data.get(k) for k in keys})

    @dataclass
    class PoorManga:  # pylint: disable=too-few-public-methods,too-many-instance-attributes
        """
        Represents an manga object from the Shikimori API.
        """

        id: int
        name: str
        russian: str
        image: dict
        url: str
        kind: str
        score: str
        status: str
        volumes: int
        chapters: int
        aired_on: str
        released_on: str

        @classmethod
        def from_json(cls, data: dict):
            """
            Converts a JSON object to a `PoorManga` object.
            """
            keys = [f.name for f in fields(cls)]

            return cls(**{k: data.get(k) for k in keys})

    import json  # pylint: disable=import-outside-toplevel

    import requests  # pylint: disable=import-outside-toplevel,import-error
    from requests.adapters import (  # pylint: disable=import-outside-toplevel,import-error
        HTTPAdapter,
        Retry,
    )

    def json_get(url: str, headers: dict) -> str:
        """
        Makes a GET request to the provided URL and returns the JSON response.

        @link https://stackoverflow.com/a/35636367
        """
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

    import jsonlines  # pylint: disable=import-outside-toplevel,import-error

    def subprocess(
        entity: str, entity_class: object, file_path: dsl.InputPath("jsonl")
    ):
        """
        Grabs the pages for the provided entity and writes them to a JSONL file.
        """
        start_url = f"{base_url}/api/{entity}?order=id&limit=1&page=0"
        end_url = f"{base_url}/api/{entity}?order=id_desc&limit=1&page=0"

        start_data = json_get(start_url, base_headers)
        end_data = json_get(end_url, base_headers)

        start_anime = entity_class.from_json(json.loads(start_data)[0])
        end_anime = entity_class.from_json(json.loads(end_data)[0])

        to_go = end_anime.id - start_anime.id
        pages = to_go // page_size + 1

        if is_testing:
            pages = 10

        with jsonlines.open(file_path, "w") as writer:
            for i in range(pages):
                page_url = (
                    f"{base_url}/api/{entity}?order=id&limit={page_size}&page={i}"
                )
                print(f"Getting {entity} page", i, "of", pages)

                page_data = json_get(page_url, base_headers)
                page_json = json.loads(page_data)

                for anime in page_json:
                    writer.write(anime)

    subprocess("animes", PoorAnime, anime_path)
    subprocess("mangas", PoorManga, manga_path)
