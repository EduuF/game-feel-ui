<div align="center">

# game-feel-ui

**Física Tátil de Jogos, Microinterações e Áudio Procedural para Interfaces Web & Mobile**

[![Live Playground](https://img.shields.io/badge/▶_Laboratório_Interativo_Ao_Vivo-eduuf.github.io%2Fgame--feel--ui-ffffff?style=for-the-badge&logoColor=black)](https://eduuf.github.io/game-feel-ui/)

[![CI Validation](https://github.com/EduuF/game-feel-ui/actions/workflows/ci.yml/badge.svg)](https://github.com/EduuF/game-feel-ui/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)
[![Mechanics](https://img.shields.io/badge/Mecânicas-39-22c55e.svg)](./data/mechanics.csv)
[![Stacks](https://img.shields.io/badge/Stacks-11-38bdf8.svg)](./data/stacks/)
[![External Audio Assets](https://img.shields.io/badge/Assets_de_Áudio-0_KB_(Web_Audio_API)-f59e0b.svg)](./references/procedural-web-audio.md)

[English](./README.md) · **Português (PT-BR)** · [**Demonstração Interativa Ao Vivo ↗**](https://eduuf.github.io/game-feel-ui/)

</div>

---

## ▶ Teste as Demonstrações Interativas Primeiro

Compare **UI Linear Comum vs. Game Feel UI** lado a lado direto no seu navegador (com telemetria em tempo real e sintetizador Web Audio sem arquivos externos):

👉 **[https://eduuf.github.io/game-feel-ui/](https://eduuf.github.io/game-feel-ui/)**

---

## Instalação Rápida

Instale no **Claude Code**, **Cursor**, **Windsurf** ou qualquer agente compatível com o padrão `skills`:

```bash
npx skills add EduuF/game-feel-ui
```

<details>
<summary><strong>Instalação Manual (Claude Code Local / Global)</strong></summary>

```bash
# No escopo de um projeto específico
git clone https://github.com/EduuF/game-feel-ui.git .claude/skills/game-feel-ui

# Ou globalmente (disponível em todos os seus projetos)
git clone https://github.com/EduuF/game-feel-ui.git ~/.claude/skills/game-feel-ui
```
</details>

---

## Por que `game-feel-ui`?

Desenvolvedores de jogos dedicam meses refinando os primeiros **50ms a 150ms** de cada comando do jogador — aplicando técnicas batizadas por Steve Swink (*Game Feel*) e Martin Jonasson & Petri Purho (*Juice it or lose it*) para que elementos virtuais transmitam massa, tensão e atrito físico real.

A maioria dos webapps parece "morta" porque os cliques trocam estados instantaneamente ou usam transições lineares (`ease-in-out`) sem antecipação, sem recuo elástico e com áreas de clique punitivas.

A `game-feel-ui` equipa agentes de código com um **motor de busca BM25 determinístico**, **auditor estático de código** e **39 mecânicas de Game Dev** traduzidas para componentes modernos:

| Técnica de Game Dev | O que faz nos Jogos | Tradução para Web & Mobile UI |
| :--- | :--- | :--- |
| **Anticipation (Antecipação)** | O personagem flexiona o corpo ou carrega a varinha antes do disparo. | **Compressão Tátil (`scale(0.95)`)** no `pointerdown` antes de disparar a ação no `pointerup`. |
| **Hitstop / Freeze Frames** | Congela a tela por 3–5 frames no impacto da espada para dar peso ao golpe. | **Micro-Pausa Pré-Recompensa (60–90ms)** no pico da compressão antes de expandir no estado de sucesso. |
| **Squash & Stretch** | O projétil estica em alta velocidade e achata no impacto. | **Spring Overshoot (`cubic-bezier(0.34, 1.56, 0.64, 1)`)**: modais, toggles e badges passam 3–5% do tamanho final e assentam. |
| **Coyote Time & Input Buffering** | Permite pular até 120ms após sair da borda da plataforma. | **Perdão Invisível**: 160ms de tolerância em menus hover, área de clique expandida (`hit-slop`) e Optimistic UI com undo. |
| **Hold-to-Commit Tension** | Carregar um golpe forte com subida de tom e tremor. | **Ações Destrutivas sem Modal**: segurar o botão "Excluir" preenche uma barra de tensão com reversão suave se soltar antes. |
| **Pitch Escalation** | Coletar moedas em sequência sobe a nota musical a cada moeda. | **Combo em Checklists e Kanban**: ações seguidas sobem `+2 semitons` (`f0 * 2^(n/12)`) via Web Audio API. |
| **Recoil & Knockback** | O atirador recua; o alvo treme ao ser atingido. | **Error Shake Amortecido (`±6px → 0px`)** em inputs inválidos e reação elástica dos cards vizinhos. |

---

## Como Usar no Claude Code & Cursor

Após instalada, a skill é acionada automaticamente quando você pede para polir, auditar ou criar interações.

### Exemplos de Prompts

```text
"Faça uma auditoria nos componentes do nosso dashboard com a game-feel-ui e aplique as 3 melhorias de maior impacto."
```

```text
"Substitua o modal de confirmação do botão de Excluir API Key por um botão Hold-to-Commit com tensão física."
```

```text
"Adicione física de mola sutil, Coyote Time nos menus dropdown e áudio procedural opcional no nosso quadro Kanban."
```

### Ferramentas CLI (Auditoria, Blueprint e Busca BM25)

```bash
# 1. Auditar um projeto existente (calcula o Juice Score de 0 a 100 e aponta arquivo:linha)
python scripts/search.py --audit ./src

# 2. Gerar um Blueprint calibrado com os 3 Dials
python scripts/search.py "b2b saas kanban" --blueprint --juice 5 --forgiveness 8 --audio 3

# 3. Persistir o Blueprint no projeto em game-feel-system/MASTER.md
python scripts/search.py "fintech checkout" --blueprint --juice 4 --forgiveness 9 --audio 2 --persist -p "CheckoutApp"
```

---

## Licença

MIT © [Eduardo Fiuza](https://github.com/EduuF)
