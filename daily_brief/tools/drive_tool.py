def search_drive_docs(query: str) -> dict:
    """
    Searches Google Drive for documents related to the query.
    NOTE: This is a stub — Google Drive requires OAuth/GCP credentials.
    Implement in a future iteration by adding OAuth2 via google-auth-oauthlib.
    """
    return {
        "status": "not_configured",
        "message": (
            f"Google Drive is not configured in this PoC. "
            f"Suggested manual search: '{query}'"
        ),
    }
