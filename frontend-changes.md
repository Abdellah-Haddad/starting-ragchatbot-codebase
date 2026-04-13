# Frontend Changes

## Code Quality Tooling

### What was added

| File | Purpose |
|---|---|
| `frontend/package.json` | npm project manifest with Prettier and ESLint as dev dependencies |
| `frontend/.prettierrc` | Prettier configuration |
| `frontend/.eslintrc.json` | ESLint configuration |
| `frontend/.prettierignore` | Excludes `node_modules/` from formatting |
| `scripts/check-frontend.sh` | Shell script that runs both Prettier and ESLint |

### Prettier (`frontend/.prettierrc`)

Prettier is the JavaScript/CSS/HTML equivalent of Black — it enforces a single, consistent code style with no configuration debates.

Settings chosen to match the existing code style:
- `singleQuote: true` — use single quotes (already used throughout)
- `semi: true` — require semicolons
- `tabWidth: 2` — 2-space indentation
- `trailingComma: "es5"` — trailing commas in objects/arrays (ES5-safe)
- `printWidth: 100` — line length limit
- `arrowParens: "always"` — always parenthesise arrow function params: `(x) => x`

### ESLint (`frontend/.eslintrc.json`)

Catches real bugs and enforces best practices in `script.js`:
- `eqeqeq` — require `===` instead of `==`
- `no-var` — disallow `var`, enforcing `const`/`let`
- `prefer-const` — warn when `let` could be `const`
- `no-unused-vars` — warn on unused variables
- `no-implicit-globals` — prevent accidental globals

`marked` (loaded from CDN) is declared as a global so ESLint does not flag it as undefined.

### `script.js` formatting changes applied

Prettier was applied to `script.js`. Key diffs from the original:

1. **Indentation normalised to 2 spaces** throughout (was 4 spaces).
2. **Trailing commas** added in multi-line objects:
   - `{ 'Content-Type': 'application/json' }` fetch header object
   - `{ query, session_id }` request body object
3. **Arrow function parentheses** made consistent: `s =>` → `(s) =>`, `.forEach(button =>` → `.forEach((button) =>`
4. **Double blank lines** collapsed to single blank lines (e.g. in `setupEventListeners`).
5. **Method chains** reformatted: `sources.map(...).join('')` broken across lines for readability.
6. **`addMessage` long string call** broken into multi-line form with trailing argument style.

### Running quality checks

**Install dependencies (once):**
```bash
cd frontend && npm install
```

**Check formatting and linting:**
```bash
# From repo root:
./scripts/check-frontend.sh

# Or from frontend/:
npm run quality
```

**Auto-fix all issues:**
```bash
# From repo root:
./scripts/check-frontend.sh --fix

# Or from frontend/ (format then lint-fix):
npm run format
npm run lint:fix
```

**Individual commands:**
```bash
cd frontend

npm run format        # apply Prettier formatting
npm run format:check  # check formatting without writing
npm run lint          # run ESLint
npm run lint:fix      # run ESLint with auto-fix
npm run quality       # format:check + lint (CI-safe, no writes)
```
