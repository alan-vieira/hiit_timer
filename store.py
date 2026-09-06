"""
Store global - Estado compartilhado.
"""

import flet as ft
from dataclasses import dataclass, field
from typing import Optional
from workout import gerar_etapas, tempo_total_estimado, WorkoutConfig


@ft.observable
@dataclass
class HIITStore:
    config: WorkoutConfig = field(default_factory=WorkoutConfig)
    num_ciclos: int = 3
    etapas: list = field(default_factory=list)
    indice_etapa_atual: int = 0
    treino_em_andamento: bool = False
    treino_finalizado: bool = False

    def __post_init__(self):
        self.atualizar_etapas()

    def atualizar_etapas(self):
        self.etapas = gerar_etapas(self.config, self.num_ciclos)
        self.indice_etapa_atual = 0
        self.treino_finalizado = False

    def reiniciar_treino(self, num_ciclos=None):
        if num_ciclos is not None:
            self.num_ciclos = num_ciclos
        self.atualizar_etapas()
        self.treino_em_andamento = True

    def finalizar_treino(self):
        self.treino_em_andamento = False
        self.treino_finalizado = True

    def voltar_config(self):
        self.treino_em_andamento = False
        self.treino_finalizado = False
        self.indice_etapa_atual = 0

    @property
    def tempo_total_seg(self) -> int:
        return tempo_total_estimado(self.config, self.num_ciclos)


store = HIITStore()