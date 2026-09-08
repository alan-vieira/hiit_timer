"""
Unit tests for store.py - State management and persistence.
Tests cover: HIITStore initialization, config loading/saving, state transitions.
"""
import pytest
import json
from unittest.mock import Mock, patch, MagicMock
from dataclasses import asdict

from store import HIITStore
from workout import WorkoutConfig, ExercicioConfig, gerar_etapas


# ============================================================================
# HIITStore Initialization Tests
# ============================================================================

class TestHIITStoreInit:
    """Tests for HIITStore initialization."""

    def test_init_defaults(self):
        """Store initializes with default values."""
        store = HIITStore()
        assert store.num_ciclos == 3
        assert store.treino_em_andamento is False
        assert store.treino_finalizado is False
        assert store.indice_etapa_atual == 0
        assert isinstance(store.config, WorkoutConfig)
        assert len(store.config.exercicios) == 5

    def test_post_init_gerar_etapas(self):
        """__post_init__ generates etapas from default config (3 cycles default)."""
        store = HIITStore()
        assert len(store.etapas) == 30  # 3 cycles default = 30 etapas
        assert store.indice_etapa_atual == 0
        assert store.treino_finalizado is False

    def test_attach_page_carrega_storage(self, mock_page_with_storage):
        """attach_page loads config from client_storage."""
        store = HIITStore()
        store.attach_page(mock_page_with_storage)

        assert len(store.config.exercicios) == 2
        assert store.config.exercicios[0].nome == "Polichinelo"
        assert store.config.exercicios[1].nome == "Elevação de joelhos"
        assert store.num_ciclos == 3

    def test_attach_page_sem_storage(self, mock_page):
        """attach_page with no saved data uses defaults."""
        store = HIITStore()
        store.attach_page(mock_page)

        assert len(store.config.exercicios) == 5
        assert store.num_ciclos == 3

    def test_attach_page_storage_corrompido(self, mock_page):
        """attach_page handles corrupted storage gracefully."""
        mock_page.client_storage.get.return_value = "invalid json{"
        store = HIITStore()
        store.attach_page(mock_page)

        # Should fall back to defaults
        assert len(store.config.exercicios) == 5
        assert store.num_ciclos == 3


# ============================================================================
# Persistence Tests
# ============================================================================

class TestHIITStorePersistence:
    """Tests for storage save/load."""

    def test_salvar_no_storage_chama_client_storage(self, store_instance):
        """_salvar_no_storage calls client_storage.set for config and ciclos."""
        store_instance.config.exercicios = [
            ExercicioConfig("Test", "🧪", 30)
        ]
        store_instance.num_ciclos = 5
        store_instance._salvar_no_storage()

        store_instance._page.client_storage.set.assert_any_call(
            "workout_config",
            json.dumps({
                "exercicios": [asdict(ex) for ex in store_instance.config.exercicios],
                "descanso_curto": store_instance.config.descanso_curto,
                "descanso_ciclo": store_instance.config.descanso_ciclo,
            }, ensure_ascii=False)
        )
        store_instance._page.client_storage.set.assert_any_call("num_ciclos", "5")

    def test_salvar_sem_page_nao_faz_nada(self):
        """_salvar_no_storage does nothing if no page attached."""
        store = HIITStore()  # No page attached
        store._salvar_no_storage()  # Should not raise

    def test_carregar_sem_page_nao_faz_nada(self):
        """_carregar_do_storage does nothing if no page attached."""
        store = HIITStore()
        store._carregar_do_storage()  # Should not raise


# ============================================================================
# State Transition Tests
# ============================================================================

class TestHIITStoreStateTransitions:
    """Tests for workout state transitions."""

    def test_atualizar_etapas_regenera(self, clean_store, sample_config):
        """atualizar_etapas regenerates etapas from current config."""
        clean_store.config = sample_config
        clean_store.num_ciclos = 2
        clean_store.atualizar_etapas()

        assert len(clean_store.etapas) == 20  # 2 cycles * 10
        assert clean_store.indice_etapa_atual == 0
        assert clean_store.treino_finalizado is False

    def test_reiniciar_treino_com_num_ciclos(self, clean_store, sample_config):
        """reiniciar_treino updates num_ciclos and regenerates etapas."""
        clean_store.config = sample_config
        clean_store.reiniciar_treino(num_ciclos=4)

        assert clean_store.num_ciclos == 4
        assert len(clean_store.etapas) == 40  # 4 cycles
        assert clean_store.treino_em_andamento is True
        assert clean_store.treino_finalizado is False

    def test_reiniciar_treino_sem_num_ciclos_mantem_atual(self, clean_store, sample_config):
        """reiniciar_treino without num_ciclos keeps current value."""
        clean_store.config = sample_config
        clean_store.num_ciclos = 5
        clean_store.reiniciar_treino()

        assert clean_store.num_ciclos == 5
        assert clean_store.treino_em_andamento is True

    def test_finalizar_treino(self, clean_store, sample_config):
        """finalizar_treino sets flags correctly."""
        clean_store.config = sample_config
        clean_store.reiniciar_treino(num_ciclos=2)
        clean_store.finalizar_treino()

        assert clean_store.treino_em_andamento is False
        assert clean_store.treino_finalizado is True

    def test_voltar_config_reseta_estado(self, clean_store, sample_config):
        """voltar_config resets workout state but keeps config."""
        clean_store.config = sample_config
        clean_store.reiniciar_treino(num_ciclos=3)
        clean_store.indice_etapa_atual = 5
        clean_store.treino_em_andamento = True
        clean_store.treino_finalizado = True

        clean_store.voltar_config()

        assert clean_store.treino_em_andamento is False
        assert clean_store.treino_finalizado is False
        assert clean_store.indice_etapa_atual == 0
        # Config should be preserved
        assert clean_store.config == sample_config

    def test_tempo_total_seg_property(self, clean_store, sample_config):
        """tempo_total_seg returns correct total from config and cycles."""
        clean_store.config = sample_config
        clean_store.num_ciclos = 3
        total = clean_store.tempo_total_seg

        # 5 exercises * 60 + 4 rests * 30 + 1 cycle rest * 60 = 480 per cycle
        assert total == 1440  # 3 * 480


# ============================================================================
# Integration with Workout Logic
# ============================================================================

class TestHIITStoreIntegration:
    """Integration tests with workout module."""

    def test_fluxo_completo_treino(self, clean_store, sample_config):
        """Complete workout flow: init -> start -> finish -> config."""
        clean_store.config = sample_config

        # Start workout
        clean_store.reiniciar_treino(num_ciclos=2)
        assert clean_store.treino_em_andamento is True
        assert len(clean_store.etapas) == 20

        # Simulate completing all etapas
        clean_store.indice_etapa_atual = 19
        clean_store.finalizar_treino()
        assert clean_store.treino_finalizado is True

        # Return to config
        clean_store.voltar_config()
        assert clean_store.treino_em_andamento is False
        assert clean_store.treino_finalizado is False
        assert clean_store.indice_etapa_atual == 0

    def test_repetir_treino_mantem_config(self, clean_store, sample_config):
        """Repeating workout keeps same config and cycles."""
        clean_store.config = sample_config
        clean_store.reiniciar_treino(num_ciclos=3)

        # Simulate finish
        clean_store.finalizar_treino()

        # Repeat (like main.py repetir_treino)
        clean_store.reiniciar_treino()

        assert clean_store.num_ciclos == 3
        assert clean_store.treino_em_andamento is True
        assert len(clean_store.etapas) == 30


# ============================================================================
# Edge Cases
# ============================================================================

class TestHIITStoreEdgeCases:
    """Edge case tests."""

    def test_storage_erro_escrita_nao_quebra(self, store_instance):
        """Storage write error doesn't break app."""
        store_instance._page.client_storage.set.side_effect = OSError("Disk full")
        store_instance._salvar_no_storage()  # Should not raise

    def test_storage_erro_leitura_nao_quebra(self, mock_page):
        """Storage read error doesn't break app."""
        mock_page.client_storage.get.side_effect = OSError("Read error")
        store = HIITStore()
        store.attach_page(mock_page)  # Should not raise
        assert len(store.config.exercicios) == 5

    def test_tipos_excecao_capturados(self, mock_page):
        """Various exception types are caught during load."""
        for exc in [json.JSONDecodeError("msg", "doc", 0), ValueError(), TypeError(), KeyError(), AttributeError()]:
            mock_page.client_storage.get.side_effect = exc
            store = HIITStore()
            store.attach_page(mock_page)
            assert len(store.config.exercicios) == 5

    def test_atualizar_etapas_salva_storage(self, clean_store, sample_config):
        """atualizar_etapas calls _salvar_no_storage."""
        clean_store.config = sample_config
        clean_store._salvar_no_storage = Mock()
        clean_store.atualizar_etapas()
        clean_store._salvar_no_storage.assert_called_once()

    def test_reiniciar_treino_salva_storage(self, clean_store, sample_config):
        """reiniciar_treino with num_ciclos calls _salvar_no_storage (twice: once for num_ciclos, once in atualizar_etapas)."""
        clean_store.config = sample_config
        clean_store._salvar_no_storage = Mock()
        clean_store.reiniciar_treino(num_ciclos=4)
        assert clean_store._salvar_no_storage.call_count == 2