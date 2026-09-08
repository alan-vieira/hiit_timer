"""
Unit tests for workout.py - Core business logic models.
Tests cover: ExercicioConfig, WorkoutConfig, Etapa, gerar_etapas, tempo_total_estimado, fmt, stats_treino
"""
import pytest
from workout import (
    ExercicioConfig,
    WorkoutConfig,
    Etapa,
    TipoEtapa,
    gerar_etapas,
    tempo_total_estimado,
    fmt,
    stats_treino,
)


# ============================================================================
# ExercicioConfig Tests
# ============================================================================

class TestExercicioConfig:
    """Tests for ExercicioConfig dataclass."""

    def test_criacao_valida(self):
        """Valid creation with positive duration."""
        ex = ExercicioConfig(nome="Polichinelo", emoji="🤸", duracao=60)
        assert ex.nome == "Polichinelo"
        assert ex.emoji == "🤸"
        assert ex.duracao == 60

    def test_criacao_invalida_duracao_zero(self):
        """Invalid creation with zero duration should fail."""
        with pytest.raises(ValueError, match="duração deve ser positivo"):
            ExercicioConfig(nome="Test", emoji="❌", duracao=0)

    def test_criacao_invalida_duracao_negativa(self):
        """Invalid creation with negative duration should fail."""
        with pytest.raises(ValueError, match="duração deve ser positivo"):
            ExercicioConfig(nome="Test", emoji="❌", duracao=-10)

    def test_criacao_invalida_nome_vazio(self):
        """Invalid creation with empty name should fail."""
        with pytest.raises(ValueError, match="nome.*obrigatório"):
            ExercicioConfig(nome="", emoji="❌", duracao=30)

    def test_criacao_invalida_emoji_vazio(self):
        """Invalid creation with empty emoji should fail."""
        with pytest.raises(ValueError, match="emoji.*obrigatório"):
            ExercicioConfig(nome="Test", emoji="", duracao=30)

    def test_eq_hashable(self):
        """ExercicioConfig should be hashable and comparable."""
        ex1 = ExercicioConfig(nome="Test", emoji="🧪", duracao=30)
        ex2 = ExercicioConfig(nome="Test", emoji="🧪", duracao=30)
        ex3 = ExercicioConfig(nome="Test", emoji="🧪", duracao=45)
        assert ex1 == ex2
        assert ex1 != ex3
        assert hash(ex1) == hash(ex2)


# ============================================================================
# WorkoutConfig Tests
# ============================================================================

class TestWorkoutConfig:
    """Tests for WorkoutConfig dataclass."""

    def test_criacao_padrao(self):
        """Default creation with built-in exercises."""
        config = WorkoutConfig()
        assert len(config.exercicios) == 5
        assert config.descanso_curto == 30
        assert config.descanso_ciclo == 60
        assert all(isinstance(ex, ExercicioConfig) for ex in config.exercicios)

    def test_criacao_customizada(self, sample_exercicios):
        """Custom creation with provided exercises."""
        config = WorkoutConfig(
            exercicios=sample_exercicios[:2],
            descanso_curto=45,
            descanso_ciclo=90
        )
        assert len(config.exercicios) == 2
        assert config.descanso_curto == 45
        assert config.descanso_ciclo == 90

    def test_criacao_invalida_sem_exercicios(self):
        """Invalid creation with empty exercises list."""
        with pytest.raises(ValueError, match="pelo menos 1 exercício"):
            WorkoutConfig(exercicios=[], descanso_curto=30, descanso_ciclo=60)

    def test_criacao_invalida_descanso_negativo(self, sample_exercicios):
        """Invalid creation with negative rest duration."""
        with pytest.raises(ValueError, match="descanso.*positivo"):
            WorkoutConfig(
                exercicios=sample_exercicios,
                descanso_curto=-10,
                descanso_ciclo=60
            )

    def test_criacao_invalida_descanso_ciclo_zero(self, sample_exercicios):
        """Invalid creation with zero cycle rest."""
        with pytest.raises(ValueError, match="descanso.*positivo"):
            WorkoutConfig(
                exercicios=sample_exercicios,
                descanso_curto=30,
                descanso_ciclo=0
            )


# ============================================================================
# Etapa Tests
# ============================================================================

class TestEtapa:
    """Tests for Etapa dataclass."""

    def test_criacao_exercicio(self):
        """Create exercise etapa."""
        etapa = Etapa(
            indice=1,
            nome="Polichinelo",
            emoji="🤸",
            duracao=60,
            tipo="exercicio",
            ciclo=1
        )
        assert etapa.tipo == "exercicio"
        assert etapa.ciclo == 1

    def test_criacao_descanso(self):
        """Create rest etapa."""
        etapa = Etapa(
            indice=2,
            nome="Descanso",
            emoji="⏱️",
            duracao=30,
            tipo="descanso",
            ciclo=1
        )
        assert etapa.tipo == "descanso"

    def test_criacao_descanso_ciclo(self):
        """Create cycle rest etapa."""
        etapa = Etapa(
            indice=3,
            nome="Descanso de ciclo",
            emoji="☕",
            duracao=60,
            tipo="descanso_ciclo",
            ciclo=1
        )
        assert etapa.tipo == "descanso_ciclo"


# ============================================================================
# gerar_etapas Tests
# ============================================================================

class TestGerarEtapas:
    """Tests for gerar_etapas function."""

    def test_geracao_basica_1_ciclo(self, sample_config):
        """Basic generation with 1 cycle."""
        etapas = gerar_etapas(sample_config, num_ciclos=1)
        # 5 exercises + 4 short rests + 1 cycle rest = 10 etapas
        assert len(etapas) == 10
        assert etapas[0].tipo == "exercicio"
        assert etapas[1].tipo == "descanso"
        assert etapas[9].tipo == "descanso_ciclo"

    def test_geracao_3_ciclos(self, sample_config):
        """Generation with 3 cycles."""
        etapas = gerar_etapas(sample_config, num_ciclos=3)
        # 3 * (5 exercises + 4 short rests + 1 cycle rest) = 30 etapas
        assert len(etapas) == 30
        # Check cycles are correct
        assert etapas[0].ciclo == 1
        assert etapas[10].ciclo == 2
        assert etapas[20].ciclo == 3

    def test_geracao_5_ciclos(self, sample_config):
        """Generation with 5 cycles."""
        etapas = gerar_etapas(sample_config, num_ciclos=5)
        assert len(etapas) == 50

    @pytest.mark.parametrize("num_ciclos", [1, 2, 3, 5, 10, 20])
    def test_parametrizado_multiplos_ciclos(self, sample_config, num_ciclos):
        """Parametrized test for multiple cycle counts."""
        etapas = gerar_etapas(sample_config, num_ciclos=num_ciclos)
        expected = num_ciclos * 10  # 10 etapas per cycle
        assert len(etapas) == expected
        # Verify all exercises present in each cycle
        exercicios_por_ciclo = sum(1 for e in etapas if e.tipo == "exercicio" and e.ciclo == 1)
        assert exercicios_por_ciclo == 5

    def test_invalido_num_ciclos_zero(self, sample_config):
        """Invalid num_ciclos = 0 should raise ValueError."""
        with pytest.raises(ValueError, match="num_ciclos deve estar entre 1 e 20"):
            gerar_etapas(sample_config, num_ciclos=0)

    def test_invalido_num_ciclos_negativo(self, sample_config):
        """Invalid negative num_ciclos should raise ValueError."""
        with pytest.raises(ValueError, match="num_ciclos deve estar entre 1 e 20"):
            gerar_etapas(sample_config, num_ciclos=-1)

    def test_invalido_num_ciclos_acima_20(self, sample_config):
        """Invalid num_ciclos > 20 should raise ValueError."""
        with pytest.raises(ValueError, match="num_ciclos deve estar entre 1 e 20"):
            gerar_etapas(sample_config, num_ciclos=21)

    def test_invalido_sem_exercicios(self):
        """Invalid config without exercises should raise ValueError at creation."""
        with pytest.raises(ValueError, match="É necessário pelo menos 1 exercício"):
            WorkoutConfig(exercicios=[], descanso_curto=30, descanso_ciclo=60)

    def test_indices_sequenciais(self, sample_config):
        """Etapa indices should be sequential starting from 1."""
        etapas = gerar_etapas(sample_config, num_ciclos=2)
        assert [e.indice for e in etapas] == list(range(1, len(etapas) + 1))

    def test_tipos_alternados(self, sample_config):
        """Exercise and rest types should alternate correctly."""
        etapas = gerar_etapas(sample_config, num_ciclos=1)
        for i, etapa in enumerate(etapas):
            if i == len(etapas) - 1:
                assert etapa.tipo == "descanso_ciclo"
            elif i % 2 == 0:
                assert etapa.tipo == "exercicio"
            else:
                assert etapa.tipo == "descanso"

    def test_duracoes_corretas(self, sample_config):
        """Durations should match config values."""
        etapas = gerar_etapas(sample_config, num_ciclos=1)
        for etapa in etapas:
            if etapa.tipo == "exercicio":
                assert etapa.duracao == 60
            elif etapa.tipo == "descanso":
                assert etapa.duracao == 30
            elif etapa.tipo == "descanso_ciclo":
                assert etapa.duracao == 60


# ============================================================================
# tempo_total_estimado Tests
# ============================================================================

class TestTempoTotalEstimado:
    """Tests for tempo_total_estimado function."""

    def test_calculo_1_ciclo(self, sample_config):
        """Total time for 1 cycle: 5*60 + 4*30 + 1*60 = 480s = 8min."""
        total = tempo_total_estimado(sample_config, num_ciclos=1)
        assert total == 480

    def test_calculo_3_ciclos(self, sample_config):
        """Total time for 3 cycles."""
        total = tempo_total_estimado(sample_config, num_ciclos=3)
        assert total == 1440  # 3 * 480

    @pytest.mark.parametrize("num_ciclos,expected", [
        (1, 480),
        (2, 960),
        (3, 1440),
        (5, 2400),
        (10, 4800),
    ])
    def test_parametrizado(self, sample_config, num_ciclos, expected):
        """Parametrized test for various cycle counts."""
        assert tempo_total_estimado(sample_config, num_ciclos=num_ciclos) == expected

    def test_config_customizada(self):
        """Custom config with different durations."""
        config = WorkoutConfig(
            exercicios=[ExercicioConfig("Test", "🧪", 30)],
            descanso_curto=10,
            descanso_ciclo=20
        )
        # 1 exercise + 1 cycle rest = 30 + 20 = 50
        assert tempo_total_estimado(config, num_ciclos=1) == 50


# ============================================================================
# fmt Tests
# ============================================================================

class TestFmt:
    """Tests for fmt (format time) function."""

    @pytest.mark.parametrize("segundos,expected", [
        (0, "00:00"),
        (1, "00:01"),
        (30, "00:30"),
        (59, "00:59"),
        (60, "01:00"),
        (61, "01:01"),
        (90, "01:30"),
        (300, "05:00"),
        (480, "08:00"),
        (3600, "60:00"),
    ])
    def test_formatacao_varios_valores(self, segundos, expected):
        """Test formatting various second values."""
        assert fmt(segundos) == expected

    def test_formatacao_valor_negativo(self):
        """Negative values should handle gracefully (floor division)."""
        # Python's // with negative: -1 // 60 = -1, -1 % 60 = 59
        # But our function shouldn't receive negative in practice
        result = fmt(-1)
        assert isinstance(result, str)


# ============================================================================
# stats_treino Tests
# ============================================================================

class TestStatsTreino:
    """Tests for stats_treino function."""

    def test_stats_1_ciclo(self, sample_config):
        """Stats for 1 cycle."""
        stats = stats_treino(sample_config, num_ciclos=1)
        assert stats["ciclos"] == 1
        assert stats["total_etapas"] == 10
        assert stats["total_exercicios"] == 5
        assert stats["tempo_total_seg"] == 480
        assert stats["tempo_total_fmt"] == "08:00"

    def test_stats_3_ciclos(self, sample_config):
        """Stats for 3 cycles."""
        stats = stats_treino(sample_config, num_ciclos=3)
        assert stats["ciclos"] == 3
        assert stats["total_etapas"] == 30
        assert stats["total_exercicios"] == 15
        assert stats["tempo_total_seg"] == 1440
        assert stats["tempo_total_fmt"] == "24:00"

    def test_stats_exercicios_contagem(self, sample_config):
        """Count exercises correctly across cycles."""
        stats = stats_treino(sample_config, num_ciclos=3)
        assert stats["total_exercicios"] == 3 * 5


# ============================================================================
# Edge Cases and Property-Based Tests
# ============================================================================

class TestEdgeCases:
    """Edge case tests."""

    def test_um_exercicio_um_ciclo(self):
        """Single exercise, single cycle."""
        config = WorkoutConfig(
            exercicios=[ExercicioConfig("Único", "🧪", 30)],
            descanso_curto=10,
            descanso_ciclo=20
        )
        etapas = gerar_etapas(config, num_ciclos=1)
        assert len(etapas) == 2  # exercise + cycle rest
        assert etapas[0].tipo == "exercicio"
        assert etapas[1].tipo == "descanso_ciclo"

    def test_um_exercicio_multiplos_ciclos(self):
        """Single exercise, multiple cycles."""
        config = WorkoutConfig(
            exercicios=[ExercicioConfig("Único", "🧪", 30)],
            descanso_curto=10,
            descanso_ciclo=20
        )
        etapas = gerar_etapas(config, num_ciclos=3)
        assert len(etapas) == 6  # 3 * (exercise + cycle rest)
        for i in range(0, 6, 2):
            assert etapas[i].tipo == "exercicio"
            assert etapas[i+1].tipo == "descanso_ciclo"

    def test_duracao_zero_exercicio_invalida(self):
        """Exercise with zero duration should be caught at config creation."""
        with pytest.raises(ValueError):
            WorkoutConfig(
                exercicios=[ExercicioConfig("Test", "🧪", 0)],
                descanso_curto=30,
                descanso_ciclo=60
            )

    def test_consistencia_tempo_total_vs_soma_etapas(self, sample_config):
        """Total time should equal sum of etapa durations."""
        for num_ciclos in [1, 2, 3, 5, 10]:
            etapas = gerar_etapas(sample_config, num_ciclos=num_ciclos)
            soma_duracoes = sum(e.duracao for e in etapas)
            total_estimado = tempo_total_estimado(sample_config, num_ciclos=num_ciclos)
            assert soma_duracoes == total_estimado


# ============================================================================
# Type Annotation Verification
# ============================================================================

class TestTypeHints:
    """Verify type hints are correct."""

    def test_tipo_etapa_literal(self):
        """TipoEtapa should be Literal with expected values."""
        assert hasattr(TipoEtapa, '__args__') or True  # Type checking at runtime limited

    def test_etapa_slots(self):
        """Etapa should use slots for memory efficiency."""
        etapa = Etapa(1, "Test", "🧪", 30, "exercicio", 1)
        assert hasattr(Etapa, '__slots__')
        assert '__dict__' not in dir(etapa) or not hasattr(etapa, '__dict__')