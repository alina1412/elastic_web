def prepare_results(results) -> list[dict]:
    # id = res.get("hits", {}).get("hits", [{}])[0].get("_source", {}).get("id")
    source_res = []
    for elem in results.get("hits", {}).get("hits", [{}]):
        if elem:
            record = {
                "id": elem.get("_id"),
                "message": elem.get("_source", {}).get("message", ""),
            }
            source_res.append(record)
    return source_res
