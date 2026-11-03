import main


def test_cors_origins_keep_local_defaults(monkeypatch):
    monkeypatch.delenv("CORS_ORIGINS", raising=False)

    assert main.get_cors_origins() == main.LOCAL_CORS_ORIGINS


def test_cors_origins_include_configured_origins(monkeypatch):
    monkeypatch.setenv("CORS_ORIGINS", "https://qa.example.com, https://prod.example.com")

    assert main.get_cors_origins() == [
        *main.LOCAL_CORS_ORIGINS,
        "https://qa.example.com",
        "https://prod.example.com",
    ]


def test_cors_origins_trim_empty_and_duplicate_values(monkeypatch):
    monkeypatch.setenv(
        "CORS_ORIGINS",
        " https://qa.example.com, ,https://qa.example.com,http://localhost:5173 ",
    )

    assert main.get_cors_origins() == [
        *main.LOCAL_CORS_ORIGINS,
        "https://qa.example.com",
    ]

