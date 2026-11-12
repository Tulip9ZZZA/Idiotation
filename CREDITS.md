# CREDITS.md — dependency compliance

Idiotation stands on five engine blocks and four skill packs. **Nothing from them is
redistributed inside this repository** — this repo contains only original skill text
and scripts, plus documented protocols. This file records what each dependency is,
under what license it is used, and the rule that keeps the usage clean.

## The five engine blocks

| # | Project | Author | License | How Idiotation uses it | Compliance rule |
|---|---|---|---|---|---|
| 1 | [firecrawl](https://github.com/firecrawl/firecrawl) | Sideguide Technologies Inc. | **AGPL-3.0** | External web-scraping service: hosted API (`FIRECRAWL_API_KEY`), MCP server, or self-hosted instance. Its evidence discipline (URL + access date per claim, UNKNOWN over guesses) is embedded in `/gate-recon`. | **Never vendor, modify, or redistribute firecrawl's code inside this repo.** AGPL obligations attach to firecrawl itself, not to a repo that calls its API as a separate service. |
| 2 | [maxxing-itout](https://github.com/Tulip9ZZZA/maxxing-itout) (branch `v2-gauntlet`) | Tulip9ZZZA | **MIT** | Optional clone under `blocks/` to run the mechanical Gauntlet (Node >= 24). The five-lens + Terrain Gate *protocol* (nine hostile questions, severity mapping, pass/revise/blocked verdicts) is re-described in our own words inside `/gate-recon` and `/idea-kill`, with attribution. | MIT allows reuse with the copyright notice preserved. This file is the notice. The mechanical implementation stays in their repo. |
| 3 | [superpowers](https://github.com/obra/superpowers) | Jesse Vincent | **MIT** | Optional clone under `blocks/`. `/idea-forge` and `/idea-kill` instruct the agent to load its `brainstorming` and `writing-plans` skills; their discipline (questions before generation, spike before implementation, bite-sized testable tasks) is summarized natively when the clone is absent. | MIT. Notice preserved here. Their SKILL.md files are loaded from their clone, not copied into ours. |
| 4 | [llm-council](https://github.com/karpathy/llm-council) | Andrej Karpathy | **NONE — all rights reserved** | Only the *published idea* is used: a council of models giving parallel first opinions, then anonymized cross-review and ranking, then a chairman synthesis. Idiotation's `/idea-forge` implements that protocol with **100% original text and code**, running natively in any harness. The repo may be cloned for the visual web app, but nothing from it is copied, quoted, or vendored. | No license = no right to copy or create derivatives. We therefore copy nothing — we independently implement the described method and credit the source of the idea. This is the same relation as "a book inspired a different book." |
| 5 | [roast-room](https://github.com/nateherkai/roast-room) | AI Automation Society | **MIT** | The council *mechanics* (seats argue in rounds, a neutral Chair keeps score, quote-verification, unanimity-is-a-warning) are adapted in `/idea-roast` in our own words, with **generic judge roles** (Investor, Customer, Technical Critic, Competitor, Operator, Contrarian, Board Member) instead of their expert personas. Their repo may be cloned for the full expert-brain experience. | MIT. Notice preserved here. We do not copy their agent files, brains, or SKILL.md text. |

## The skill packs (installed globally by `scripts/install-global-skills.ps1`)

All four are MIT and are copied **as-is, unmodified**, to `~/.config/opencode/skills/`.
Attribution is written to `~/.config/opencode/skills/_credits/ATTRIBUTION.md`.

| Pack | Author | License | Global skills installed |
|---|---|---|---|
| [brand-skills](https://github.com/cofoundy/brand-skills) | Cofoundy SAC | MIT | `brand`, `brand-architecture`, `brand-audit`, `brand-context`, `brand-guidelines`, `brand-identity`, `brand-init`, `brand-messaging`, `brand-mod`, `brand-positioning`, `brand-story`, `brand-strategy`, `brand-voice`, `competitor-branding`, `naming`, `rebranding`, `target-audience` |
| [logo-design-skill](https://github.com/kaankiziltug/logo-design-skill) | kaankiziltug | MIT | `logo-design` |
| [beautify-github-readme](https://github.com/oil-oil/beautify-github-readme) | oil-oil | MIT | `beautify-github-readme` |
| [skills ("Skills For Real Engineers")](https://github.com/mattpocock/skills) | Matt Pocock | MIT | all of `engineering/*` and `productivity/*` (incl. `grill-with-docs`, `to-spec`, `to-tickets`, `tdd`, `implement`, `code-review`) |

Nested attributions preserved by their NOTICE files: brand-skills' `naming` skill is
adapted from [glacierphonk/naming](https://github.com/glacierphonk/naming) (MIT),
and brand-genesis skills from [arnabbagxd/Brand-building-skills](https://github.com/arnabbagxd/Brand-building-skills).

## The Idiotation originals

- All six `SKILL.md` files under `.opencode/skills/` (and their `.claude/skills`
  mirrors) — original text by Idiotation, describing the protocols with attribution.
- `AGENTS.md`, `PHILOSOPHY.md` (distilled from the "Good ideas" conversation),
  `docs/`, `scripts/`, `assets/` — original.
- MIT for all of it — see [`LICENSE`](LICENSE).

## If you redistribute Idiotation

You may. Keep this file, keep LICENSE, and do not start shipping copies of firecrawl
or llm-council code inside your fork — direct users to `scripts/install-blocks.ps1`
which pulls each block from its own home, per its own terms.
