import pytest
from src.rag import run_rag_web
from src import config

@pytest.mark.skipif(not config.TAVILY_API_KEY, reason="Tavily API key not set")
def test_tavily_response():
    query = "What is the latest update on cancer immunotherapy?"
    result = run_rag_web(query)

    assert result is not None, "Tavily returned None"
    assert isinstance(result, str), "Tavily result is not a string"
    assert len(result.strip()) > 0, "Tavily returned an empty string"
