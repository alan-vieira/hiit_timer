"""
Módulo de dados do treino HIIT.
"""

from dataclasses import dataclass, field
from typing import Literal

TipoEtapa = Literal["exercicio", "descanso", "descanso_ciclo"]


@dataclass
class ExercicioConfig:
    nome: str
    emoji: str
    duracao: int


@dataclass
class WorkoutConfig:
    exercicios: list = field(default_factory=lambda: [
        ExercicioConfig("Polichinelo", "\U0001f938", 60),
        ExercicioConfig("Elevação de joelhos", "\U0001f9b5", 60),
        ExercicioConfig("Crucifixo", "\U0001f98b", 60),
        ExercicioConfig("Extensão de braços", "\U0001f4aa", 60),
        ExercicioConfig("Agachamento", "\U0001f3cb\ufe0f", 60),
    ])
    descanso_curto: int = 30
    descanso_ciclo: int = 60


@dataclass(slots=True)
class Etapa:
    indice: int
    nome: str
    emoji: str
    duracao: int
    tipo: TipoEtapa
    ciclo: int


def gerar_etapas(config: WorkoutConfig, num_ciclos: int = 3) -> list:
    if not 1 <= num_ciclos <= 20:
        raise ValueError("num_ciclos deve estar entre 1 e 20")
    if not config.exercicios:
        raise ValueError("É necessário pelo menos 1 exercício")
    etapas = []
    idx_global = 0
    for ciclo in range(1, num_ciclos + 1):
        for i, ex in enumerate(config.exercicios):
            idx_global += 1
            etapas.append(Etapa(idx_global, ex.nome, ex.emoji, ex.duracao, "exercicio", ciclo))
            idx_global += 1
            if i == len(config.exercicios) - 1:
                etapas.append(Etapa(idx_global, "Descanso de ciclo", "\u2615", config.descanso_ciclo, "descanso_ciclo", ciclo))
            else:
                etapas.append(Etapa(idx_global, "Descanso", "\u23f8\ufe0f", config.descanso_curto, "descanso", ciclo))
    return etapas


def tempo_total_estimado(config: WorkoutConfig, num_ciclos: int = 3) -> int:
    return sum(e.duracao for e in gerar_etapas(config, num_ciclos))


def fmt(segundos: int) -> str:
    m = segundos // 60
    s = segundos % 60
    return f"{m:02d}:{s:02d}"


def stats_treino(config: WorkoutConfig, num_ciclos: int = 3) -> dict:
    etapas = gerar_etapas(config, num_ciclos)
    total_seg = sum(e.duracao for e in etapas)
    return {
        "ciclos": num_ciclos,
        "total_etapas": len(etapas),
        "total_exercicios": sum(1 for e in etapas if e.tipo == "exercicio"),
        "tempo_total_seg": total_seg,
        "tempo_total_fmt": fmt(total_seg),
    }