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
|- agent-reflection/
   |- example_1/
   |  |- agent_reflection.py
   |  |- requirements.txt
   |  |- sri_lanka_inflation_2024_2025.csv
   |  |- chart_v1.png
   |  |- chart_v2.png
   |- example_2/
      |- agent_reflection_v2.py
      |- requirements.txt
      |- utils.py
|- agent-tools-selection/
   |- example_1/
      |- agent_tools_selection.py
```

## Reflection Example

Location: `agent-reflection/example_1/`

The script in `agent-reflection/example_1/agent_reflection.py`:
- Loads inflation data from `sri_lanka_inflation_2024_2025.csv`.
- Prompts a model to generate plotting code.
- Executes generated code to create `chart_v1.png`.
- Sends the chart and code to a second model for critique and improvement.
- Executes the refined code to create `chart_v2.png`.

## Before and After Reflection

The images below show the output before and after the reflection pass.

| Before Reflection | After Reflection |
| --- | --- |
| ![Chart v1](agent-reflection/example_1/chart_v1.png) | ![Chart v2](agent-reflection/example_1/chart_v2.png) |

The first chart is the initial model output. The second chart is the revised version after critique and improvement.

## 2. Tools Use

The tools-use example shows how an agent can select and call functions from a predefined tool set.

Location: `agent-tools-selection/example_1/`

The script in `agent_tools_selection.py`:
- Gets the current time.
- Fetches weather for the user’s location from their IP address.
- Writes the weather summary to a text file.
- Generates a QR code for a website, using an optional embedded image.

This example demonstrates basic tool selection, function calling, and tool-result handling in a single workflow.

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

To run the tools-use example, move into `agent-tools-selection/example_1` and run `agent_tools_selection.py`.

## Notes

- The reflection pattern is useful when first-pass outputs are acceptable but not polished.
- A stronger critique stage often improves clarity, correctness, and presentation quality.
- This repo is structured as a learning project, so each pattern can live in its own folder with runnable examples.

## Next Improvements (Optional)

- Add error handling around model output parsing.
- Add a validation step before executing generated code.
- Add automated checks to compare chart quality between versions.
- Add more design patterns (planning, tool use, multi-agent orchestration).

