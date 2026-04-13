import pytest
from unittest.mock import MagicMock
from vector_store import SearchResults


# ---------------------------------------------------------------------------
# Shared sample data
# ---------------------------------------------------------------------------

SAMPLE_CHROMA_RESULTS = {
    "documents": [["Lesson content about Python basics.", "More content here."]],
    "metadatas": [[
        {"course_title": "Python Fundamentals", "lesson_number": 1, "chunk_index": 0},
        {"course_title": "Python Fundamentals", "lesson_number": 2, "chunk_index": 0},
    ]],
    "distances": [[0.12, 0.34]],
}


# ---------------------------------------------------------------------------
# SearchResults fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def sample_search_results():
    """Two-document SearchResults with full metadata."""
    return SearchResults.from_chroma(SAMPLE_CHROMA_RESULTS)


@pytest.fixture
def empty_search_results():
    """Empty SearchResults with no error."""
    return SearchResults(documents=[], metadata=[], distances=[])


@pytest.fixture
def error_search_results():
    """SearchResults carrying a ChromaDB error string."""
    return SearchResults.empty(
        "Search error: Number of requested results 5 is greater than number of elements in index 0"
    )


# ---------------------------------------------------------------------------
# VectorStore mock fixture
# ---------------------------------------------------------------------------

@pytest.fixture
def mock_vector_store(sample_search_results):
    """
    MagicMock standing in for VectorStore.
    Defaults: .search() returns sample_search_results, .get_lesson_link() returns a URL.
    """
    store = MagicMock()
    store.search.return_value = sample_search_results
    store.get_lesson_link.return_value = "https://example.com/lesson/1"
    store.get_course_outline.return_value = None
    return store


# ---------------------------------------------------------------------------
# Anthropic response mock helpers (module-level, importable by test files)
# ---------------------------------------------------------------------------

def make_text_response(text: str):
    """Create a mock Anthropic Message with a single text block and stop_reason=end_turn."""
    block = MagicMock()
    block.type = "text"
    block.text = text
    response = MagicMock()
    response.stop_reason = "end_turn"
    response.content = [block]
    return response


def make_tool_use_response(tool_name: str, tool_input: dict, tool_use_id: str = "tu_abc123"):
    """Create a mock Anthropic Message that requests a tool call."""
    block = MagicMock()
    block.type = "tool_use"
    block.name = tool_name
    block.input = tool_input
    block.id = tool_use_id
    response = MagicMock()
    response.stop_reason = "tool_use"
    response.content = [block]
    return response
