# AGENTS.md

## Setup commands
- Install deps: `pnpm install`
- Start dev server: `pnpm dev`
- Run tests: `pnpm test`

## Code style
- TypeScript strict mode
- Single quotes, no semicolons
- Use functional patterns where possible

## Django Project Conventions

- **Initial Data**: Use Django fixtures to populate initial database data. Place fixture files in the `fixtures` directory of the relevant app (e.g., `bio/fixtures/bio_data.json`). Load data using the `./manage.py loaddata <fixture_name>` command.
- **Styling**: Tailwind CSS is available via the base template. Use it for styling, but adhere to a principle of minimal CSS. Only apply essential classes for layout and basic component styling.