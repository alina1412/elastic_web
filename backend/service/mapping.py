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
      "filter": {
        "russian_stop": {
          "type":       "stop",
          "stopwords":  "_russian_" 
        },
        "russian_keywords": {
          "type":       "keyword_marker",
          "keywords":   ["пример"] 
        },
        "russian_stemmer": {
          "type":       "stemmer",
          "language":   "russian"
        }
      },
      "analyzer": {
        "my_analyzer": {
          "tokenizer":   "edge_ngram_tokenizer",
          "filter": [
            "lowercase",
            "russian_stop",
            "russian_keywords",
            "russian_stemmer"
          ]
        },
      },
       "tokenizer": {
          "edge_ngram_tokenizer": {
            "type": "edge_ngram",
            "min_gram": 3,
            "max_gram": 15,
            "token_chars": [
              "letter", 
              "digit"
            ]
          }
        }
    }
}

# fmt: on
