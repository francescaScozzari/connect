"""Scopus utils."""


def is_orcid_id(_id: int | str) -> bool:
    """Tell whether the provided id is an ORCID id."""
    try:
        int(_id)
    except ValueError:
        return True
    return False
