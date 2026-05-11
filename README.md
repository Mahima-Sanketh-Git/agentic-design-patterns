# Agentic AI Design Patterns

A hands-on learning repository for implementing common agentic AI design patterns in Python.

## 1. Reflection

Reflection is an agentic pattern where an AI system improves its own output through a second-pass critique.

In this project, the flow is:
1. A fast model generates initial matplotlib code to visualize Sri Lanka inflation data.
2. The generated code is executed to create an initial chart (`chart_v1.png`).
3. A second model reviews both the chart and the first code draft.
4. The system regenerates improved chart code and produces a refined chart (`chart_v2.png`).

This demonstrates how reflection can improve output quality with a critique-and-revise loop.

## Project Structure

```text
agent-design-pattern/
|- README.md
|- requirements.txt
|- agent-reflection/
   |- agent_reflection.py
   |- requirements.txt
   |- sri_lanka_inflation_2024_2025.csv
```

## Reflection Example

Location: `agent-reflection/`

The script in `agent_reflection.py`:
- Loads inflation data from `sri_lanka_inflation_2024_2025.csv`.
- Prompts a model to generate plotting code.
- Executes generated code to create `chart_v1.png`.
- Sends the chart and code to a second model for critique and improvement.
- Executes the refined code to create `chart_v2.png`.

## Setup

### 1. Create and activate a virtual environment (recommended)

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
pip install -r agent-reflection/requirements.txt
```

### 3. Add your API key

Create a `.env` file in the project root with:

```env
GEMINI_API_KEY=your_api_key_here
```

## Run the Reflection Demo

From the project root:

```powershell
cd agent-reflection
python agent_reflection.py
```

If successful, the script will generate or update:
- `chart_v1.png`
- `chart_v2.png`

## Notes

- The reflection pattern is useful when first-pass outputs are acceptable but not polished.
- A stronger critique stage often improves clarity, correctness, and presentation quality.
- This repo is structured as a learning project, so each pattern can live in its own folder with runnable examples.

## Next Improvements (Optional)

- Add error handling around model output parsing.
- Add a validation step before executing generated code.
- Add automated checks to compare chart quality between versions.
- Add more design patterns (planning, tool use, multi-agent orchestration).
