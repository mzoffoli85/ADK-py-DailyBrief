def search_drive_docs(query: str) -> dict:
    """
    Busca documentos en Google Drive relacionados con la consulta.
    NOTA: Esta es una implementación stub — Google Drive requiere credenciales OAuth/GCP.
    Implementar en una iteración futura usando OAuth2 con google-auth-oauthlib.
    """
    return {
        "status": "not_configured",
        "message": (
            f"Google Drive no está configurado en este PoC. "
            f"Búsqueda manual sugerida: '{query}'"
        ),
    }
