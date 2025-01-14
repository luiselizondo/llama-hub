# Elasticsearch7 Loader

The Elasticsearch7 Loader returns a set of texts corresponding to documents retrieved from an Elasticsearch index.
The user initializes the loader with an Elasticsearch index. They then pass in a field, and optionally a JSON query DSL object to fetch the fields they want.
It uses Elasticsearch Version 7.9.1

## Usage

Here's an example usage of the ElasticsearchReader to load 100 documents.

```python
from llama_index import download_loader

ElasticsearchReaderRest = download_loader("ElasticsearchReaderRest")

reader = ElasticsearchReaderRest(
    "http://localhost:9200",
    index_name,
)


query_dict = {"query": {"match": {"message": {"query": "this is a test"}}}}
documents = reader.load_data(
    "<field_name>", query=query_dict, embedding_field="field_name", size=100
)
```

This loader is designed to be used as a way to load data into [LlamaIndex](https://github.com/run-llama/llama_index/tree/main/llama_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent. See [here](https://github.com/emptycrown/llama-hub/tree/main) for examples.
