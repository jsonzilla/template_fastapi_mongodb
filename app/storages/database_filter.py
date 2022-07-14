from flatdict import FlatterDict


def format_to_database_filter(data: dict) -> dict:
    """ Format to MongoDb database filter. """
    result = FlatterDict(data, delimiter='.')
    result = _remove_empty(result)
    return dict(result)


def _remove_empty(data):
    """ Remove empty values from dict. """
    for k, v in data.items():
        if isinstance(v, dict):
            _remove_empty(v)
        if not v:
            del data[k]
    return data


def format_pages_to_filter(per_page: int, page: int, filter: list):
    """ Format pages to filter. """
    if not page or page <= 0:
        page = 1
    if not per_page or per_page <= 0:
        per_page = 50
    if per_page:
        filter.append({"$skip": per_page * (page - 1)})
        filter.append({"$limit": per_page})
