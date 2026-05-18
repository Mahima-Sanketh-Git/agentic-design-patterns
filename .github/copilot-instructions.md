# GitHub Copilot Instructions — Industry Standard README Generator

Place this file at `.github/copilot-instructions.md` in your repository.
Copilot will automatically pick it up as workspace context.

---

## 🧭 Instructions for Copilot

When I ask you to **generate**, **create**, or **update** a README, follow every rule in this file precisely.

---

## 📋 README Structure (Always follow this exact order)

Generate a README with these sections in this order — skip a section only if there is genuinely no relevant content for it:

```
1.  Project Banner / Hero (badges + title + tagline)
2.  Table of Contents
3.  Overview
4.  Features
5.  Tech Stack
6.  Project Structure
7.  Prerequisites
8.  Installation
9.  Configuration (.env / environment variables)
10. Usage / Quick Start
11. API Reference (if applicable)
12. Scripts
13. Testing
14. Deployment
15. Contributing
16. License
17. Acknowledgements (if applicable)
```

---

## 📐 Section-by-Section Rules

### 1. Project Banner / Hero
- Use the project name as an `<h1>` with an emoji that matches the domain
- Write a **one-line tagline** — sharp, no fluff
- Include shields.io badges for: build status, license, node version, npm version (use relevant ones only)
- Example badge format:
  ```md
  <img src="https://img.shields.io/badge/license-MIT-blue.svg">
  <img src="https://img.shields.io/badge/node-%3E%3D18.0.0-brightgreen">
  ```

### 2. Table of Contents
- Auto-linked to every H2 section
- Use GitHub anchor format: `[Section](#section-name)`

### 3. Overview
- 2–4 sentences MAX
- Answer: **what** it does, **who** it's for, **why** it exists
- No marketing fluff — be technical and direct

### 4. Features
- Bullet list, each item starts with a relevant emoji
- Each feature is one line — no nested bullets
- Max 8 features

### 5. Tech Stack
- Use a markdown table with columns: **Technology**, **Purpose**, **Version**
- List only direct dependencies — not transitive ones

### 6. Project Structure
- Use a code block with directory tree
- Add inline comments explaining each folder/file's purpose
- Example:
  ```
  src/
  ├── agent.ts        # Main LLM agent loop
  ├── client.ts       # MCP client setup
  └── tools/
      └── weather.ts  # Weather tool definition
  ```

### 7. Prerequisites
- Bullet list of exact tools + minimum versions required
- Include links to installation pages

### 8. Installation
- Numbered steps only — no prose
- Include the exact commands to run, wrapped in code blocks with language tags
- Always include: clone → install → build steps

### 9. Configuration
- Show a complete `.env.example` block
- For each variable: name, description, whether required or optional, example value
- Use a markdown table format:

  | Variable | Description | Required | Example |
  |----------|-------------|----------|---------|
  | `API_KEY` | Your API key | ✅ | `sk-abc123` |

### 10. Usage / Quick Start
- Show the minimal commands to get it running
- Include expected terminal output as a code block with `# output` comments

### 11. API Reference (if applicable)
- One subsection per endpoint or public function
- Include: method, path, description, request body (if any), response example

### 12. Scripts
- Table format: **Script**, **Command**, **Description**
- List every script in `package.json` or `Makefile`

### 13. Testing
- How to run tests
- What testing framework is used
- How to run with coverage

### 14. Deployment
- Step-by-step for the most common deployment target
- Include environment-specific notes if relevant

### 15. Contributing
- Link to `CONTRIBUTING.md` if it exists, otherwise include:
  - Fork → branch → commit → PR flow
  - Commit message convention (use Conventional Commits)
  - Branch naming: `feat/`, `fix/`, `docs/`, `chore/`

### 16. License
- One line: `Distributed under the MIT License. See LICENSE for more information.`
- Always match the actual license in the repo

---

## ✍️ Writing Style Rules

- **Voice**: Direct, technical, no marketing language
- **Tense**: Present tense always (`Returns`, not `Will return`)
- **Tone**: Professional but not robotic — write like a senior engineer wrote it
- **Length**: Sections should be as short as possible while being complete
- **Never write**: "This project is a powerful tool that...", "Leveraging cutting-edge...", "Seamlessly integrates..."
- **Always write**: Concrete, specific descriptions of what things do

---

## 🏷️ Formatting Rules

- Every code block must have a language tag: ` ```typescript `, ` ```bash `, ` ```json `
- All file paths must be wrapped in backticks: `src/agent.ts`
- All environment variables must be wrapped in backticks: `GEMINI_API_KEY`
- Use `>` blockquotes for important notes or warnings
- Use `---` horizontal rules between major sections

---

## 🚀 Prompt to Use

When ready, give Copilot this prompt:

```
Generate a complete, industry-standard README.md for this project following 
the rules in .github/copilot-instructions.md.

Scan the entire codebase including:
- package.json files (name, scripts, dependencies, version)
- All source files in src/ or apps/
- Any existing .env.example or config files
- tsconfig.json files

Then produce a README.md with every applicable section filled in with 
accurate, specific information from the actual code — no placeholder text, 
no generic descriptions. Every command must be real and runnable.
```

---

## Constraints
- Never expose API keys in README file

## ⚡ Quick Inline Prompts (use these in editor)

```
// Generate README section: Installation
// Generate README section: API Reference for this file
// Generate README section: Project Structure for this monorepo
// Update README Tech Stack table based on package.json dependencies
// Generate .env.example from all process.env usages in this codebase
```
