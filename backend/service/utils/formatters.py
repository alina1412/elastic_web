def prepare_results(results) -> list[dict]:
    # id = res.get("hits", {}).get("hits", [{}])[0].get("_source", {}).get("id")
    source_res = []
    for elem in results.get("hits", {}).get("hits", [{}]):
        source_res.append(elem["_source"])
    return source_res
