responses = {
    200: {
        "description": "Random anime information retrieved successfully.",
    },
    404: {
        "description": "Anime not found.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Anime not found.",
                }
            }
        }
    },
    429: {
        "description": "Too many requests.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Too many requests.",
                }
            }
        }
    }
}