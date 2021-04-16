import urllib, json

def extract_json_values(obj: dict, key: str) -> list:
    """
    Pull all values of specified key from nested JSON.

    Args:
        obj (dict): nested dict
        key (str): name of key to pull out

    Returns:
        list: values for the specified key
    """
    arr = []

    def extract(obj, arr, key):
        """ Recursively search for values of key in JSON tree. """
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    results = extract(obj, arr, key)
    return results


def get_qid_from_wikipedia_id(wikipedia_id: str) -> str:
    """
    Given a Wikipedia ID e.g. Joseph_Lister, return the Wikidata QID.

    Args:
        url (str)
    Returns:
        qid (str)
    """
    # passing the redirects param through the API gets the details of the page that Wikipedia may redirect to
    endpoint = (
                    "https://en.wikipedia.org/w/api.php?action=query&prop=pageprops&titles="
                    + wikipedia_id
                    + "&format=json&redirects"
                )
    res = urllib.request.urlopen(endpoint)
    res_body = res.read()
    data = json.loads(res_body.decode("utf-8"))
    wikibase_item = extract_json_values(data, "wikibase_item")
    
    return wikibase_item[0] if len(wikibase_item) > 0 else None
    
