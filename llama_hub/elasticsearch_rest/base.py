"""Elasticsearch (or Opensearch) reader over REST api.

This only uses the basic search api, so it will work with Elasticsearch and Opensearch.

"""

from typing import List, Optional

from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document


class ElasticsearchReaderRest(BaseReader):
    """
    Read documents from an Elasticsearch/Opensearch index.

    These documents can then be used in a downstream Llama Index data structure.

    Args:
        endpoint (str): URL (http/https) of cluster without port
        index (str): Name of the index (required)
        basic_auth (set): basic authentication username password
    """

    def __init__(self, endpoint: str, index: str, basic_auth: Optional[set] = None):
        """Initialize with parameters."""
        import requests

        self._post = requests.post
        self._basic_auth = basic_auth
        self._index = index
        self._endpoint = endpoint

    def load_data(
        self,
        field: str,
        query: Optional[dict] = None,
        embedding_field: Optional[str] = None,
    ) -> List[Document]:
        """Read data from the Elasticsearch index.

        Args:
            field (str): Field in the document to retrieve text from
            query (Optional[dict]): Elasticsearch JSON query DSL object.
                For example:
                { "query" : {"match": {"message": {"query": "this is a test"}}}}
            embedding_field (Optional[str]): If there are embeddings stored in
                this index, this field can be used
                to set the embedding field on the returned Document list.
        Returns:
            List[Document]: A list of documents.

        """
        query = (
            query["query"] if query is not None else None
        )  # To remain backward compatible

        response = self._post(self._endpoint + "/" + self._index + "/_search", json=query)
        if response.status_code != 200:
            optional_detail = response.json().get("error")
            raise ValueError(
                f" Call failed with status code {response.status_code}."
                f" Details: {optional_detail}"
            )

        res = response.json()
        documents = []
        for hit in res["hits"]["hits"]:
            value = hit["_source"][field]
            _ = hit["_source"].pop(field)
            embedding = hit["_source"].get(embedding_field or "", None)
            documents.append(
                Document(text=value, extra_info=hit["_source"], embedding=embedding)
            )
        return documents
