# Guia de Contribuição

Obrigado por considerar contribuir para o HIIT Timer!

## Como Reportar Bugs

1. Verifique se o bug já foi reportado nas [Issues](https://github.com/SEU_USUARIO/hiit_timer/issues)
2. Se não existe, abra uma nova issue com:
   - Título claro e descritivo
   - Passos para reproduzir
   - Comportamento esperado vs atual
   - Screenshots se aplicável
   - Versão do Python, Flet e OS

## Sugerindo Melhorias

Abra uma issue com a tag `enhancement` descrevendo:
- O problema que a melhoria resolve
- A solução proposta
- Alternativas consideradas

## Pull Requests

1. Fork o repositório
2. Crie uma branch: `git checkout -b feat/nome-da-feature` ou `fix/nome-do-bug`
3. Faça commits seguindo **Conventional Commits** (veja abaixo)
4. Rode os testes/lint localmente se existirem
5. Abra o PR contra `main` com descrição clara

## Padrão de Commits (Conventional Commits)

```
<tipo>(<escopo>): <descrição curta>

[corpo opcional]

[rodapé opcional]
```

### Tipos

| Tipo | Descrição |
|------|-----------|
| `feat` | Nova funcionalidade |
| `fix` | Correção de bug |
| `docs` | Alterações na documentação |
| `style` | Formatação, sem mudança de lógica |
| `refactor` | Refatoração de código |
| `test` | Adição/alteração de testes |
| `chore` | Tarefas de build, deps, etc |

### Exemplos

```
feat(timer): adiciona vibração na transição de fase
fix(store): corrige contagem de ciclos ao reiniciar
docs(readme): atualiza instruções de build Android
style(components): formatação black nos componentes
```

## Padrões de Código

- Python 3.12+ com type hints
- Formatação com `black` (line-length 100)
- Lint com `pylint` (score 10/10 alvo)
- Imports organizados: stdlib, third-party, local
- Docstrings em português (PT-BR) para módulos públicos

## Checklist antes do PR

- [ ] Código formata com `black`
- [ ] `pylint` sem erros novos
- [ ] Testes passam (se existirem)
- [ ] Documentação atualizada se necessário
- [ ] Commits seguem Conventional Commits