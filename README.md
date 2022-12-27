# elastic_web

Task:
Сервис, который смотрит в elasticsearch, и может создавать там базы.
- Умеет искать в созданной базе полнотектовым поиском.
- Делать это все через простейшую web-форму.

To run locally:
- create env file
- `make build` (wait for containers to start)
- run fill_index_from_csv.py
- work with http://localhost:8000/docs and web http://localhost:8080/

TODO:
- лимит.баланс памяти в эластике (починить flood stage disk watermark [95%] exceeded)