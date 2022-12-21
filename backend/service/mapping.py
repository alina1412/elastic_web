# fmt: off

mapping_for_index = {
    "properties": {
        "id": {
            "type": "integer",
            "fields": {
                "keyword": {
                    "type": "keyword"
                }
            }
        },
        "message": {
            "type": "text",
            "analyzer": "my_analyzer"
        },
    }
}

elastic_text_settings = {
    "analysis": {
        "analyzer": {
            "my_analyzer": {
                "type": "custom",
                "tokenizer": "my_tokenizer",
                "filter": [
                    "lowercase"
                ]
            }
        },
        "tokenizer": {
            "my_tokenizer": {
                "type": "edge_ngram",
                "min": 3,
                "max": 15,
                "token_chars": ["letter", "digit"]
            }
        }
    }
}
# fmt: on
