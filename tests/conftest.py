"""
Shared pytest fixtures for HIIT Timer tests.
"""
import pytest
import asyncio
import flet as ft
from unittest.mock import Mock, MagicMock, AsyncMock
from dataclasses import dataclass
from typing import Optional

from workout import (
    WorkoutConfig, ExercicioConfig, Etapa, TipoEtapa,
    gerar_etapas, tempo_total_estimado, fmt, stats_treino
)
from store import HIITStore


# ============================================================================
# Test Data Fixtures
# ============================================================================

@pytest.fixture
def sample_exercicio():
    """Sample ExercicioConfig for testing."""
    return ExercicioConfig(nome="Polichinelo", emoji="🤸", duracao=60)


@pytest.fixture
def sample_exercicios():
    """Sample list of ExercicioConfig for testing."""
    return [
        ExercicioConfig(nome="Polichinelo", emoji="🤸", duracao=60),
        ExercicioConfig(nome="Elevação de joelhos", emoji="🦵", duracao=60),
        ExercicioConfig(nome="Crucifixo", emoji="🦋", duracao=60),
        ExercicioConfig(nome="Extensão de braços", emoji="💪", duracao=60),
        ExercicioConfig(nome="Agachamento", emoji="🏋️", duracao=60),
    ]


@pytest.fixture
def sample_config(sample_exercicios):
    """Sample WorkoutConfig for testing."""
    return WorkoutConfig(
        exercicios=sample_exercicios,
        descanso_curto=30,
        descanso_ciclo=60
    )


@pytest.fixture
def sample_etapas(sample_config):
    """Sample list of Etapa for testing (3 cycles)."""
    return gerar_etapas(sample_config, num_ciclos=3)


# ============================================================================
# Mock Fixtures for Flet
# ============================================================================

@pytest.fixture
def mock_page():
    """Mock Flet Page for testing."""
    page = Mock(spec=ft.Page)
    page.client_storage = Mock()
    page.client_storage.get = Mock(return_value=None)
    page.client_storage.set = Mock()
    page.views = []
    page.route = "/config"
    page.window = Mock()
    page.window.width = 400
    page.window.height = 850
    page.window.min_width = 360
    page.window.min_height = 700
    page.window.full_screen = False
    page.window.prevent_close = False
    page.update = Mock()
    page.run_task = Mock()
    page.show_dialog = Mock()
    page.on_route_change = None
    page.on_view_pop = None
    page.on_back_button = None
    return page


@pytest.fixture
def mock_page_with_storage(mock_page):
    """Mock page with saved config in client_storage."""
    import json
    saved_config = {
        "exercicios": [
            {"nome": "Polichinelo", "emoji": "🤸", "duracao": 60},
            {"nome": "Elevação de joelhos", "emoji": "🦵", "duracao": 60},
        ],
        "descanso_curto": 30,
        "descanso_ciclo": 60,
    }
    mock_page.client_storage.get.side_effect = lambda key: (
        json.dumps(saved_config) if key == "workout_config" else "3"
    )
    return mock_page


# ============================================================================
# Store Fixtures
# ============================================================================

@pytest.fixture
def store_instance(mock_page):
    """HIITStore instance attached to mock page."""
    from store import HIITStore
    store = HIITStore()
    store.attach_page(mock_page)
    return store


@pytest.fixture
def clean_store():
    """HIITStore instance without page attachment (no persistence)."""
    from store import HIITStore
    return HIITStore()


# ============================================================================
# Async Test Utilities
# ============================================================================

@pytest.fixture
def event_loop():
    """Event loop for async tests."""
    import asyncio
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


# ============================================================================
# Test Helpers
# ============================================================================

@dataclass
class TimerState:
    """Mock timer state for testing timer_screen logic."""
    idx: int = 0
    tempo: int = 0
    pausado: bool = False
    finalizado: bool = False
    cancel: bool = False
    task: Optional[asyncio.Task] = None


# ============================================================================
# Pytest Configuration
# ============================================================================

def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line("markers", "unit: Unit tests for pure logic")
    config.addinivalue_line("markers", "ui: UI tests using Flet TestView")
    config.addinivalue_line("markers", "integration: Integration tests")
    config.addinivalue_line("markers", "slow: Tests that take > 1 second")


# ============================================================================
# Async Test Support
# ============================================================================

@pytest.fixture
def anyio_backend():
    """Use asyncio backend for pytest-asyncio."""
    return "asyncio"