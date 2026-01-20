# resumex

[![PyPI](https://img.shields.io/pypi/v/resumex-py.svg)](https://pypi.org/project/resumex-py/)
[![Tests](https://img.shields.io/github/actions/workflow/status/rsm-vsivasankaran/resumex/tests.yml?branch=main)](https://github.com/rsm-vsivasankaran/resumex/actions)

An easy, YAML-based, theme-driven resume generator. `resumex` takes your structured data and produces professional LaTeX and PDF resumes with strict schema validation.

## Features

- **YAML-first**: Store your career data in a clean, versionable format.
- **Strict Validation**: Powered by Pydantic to ensure your data matches your theme's requirements.
- **Theme System**: Fully customizable layouts using Jinja2 templates.
- **Dual Usage**: Use it via CLI or as a Python module in your own scripts.
- **Smart Compilation**: Automatically handles LaTeX runs using `latexmk` or falls back to direct engines like `pdflatex`.

## Installation

### Requirements

- **Python**: 3.12 or higher.
- **LaTeX**: A distribution (like TeX Live, MacTeX, or MiKTeX) providing `latexmk` (recommended) or `pdflatex`.

### Using `uv` (Recommended)

```bash
uv tool install resumex-py
```

### Using `pip`

```bash
pip install resumex-py
```

## Quickstart

1. **Create your resume**: Save your data in `resume.yaml` (see [examples/resume.yaml](examples/resume.yaml)).
2. **Generate PDF**:
   ```bash
   resumex build resume.yaml
   ```
3. **Generate TeX only**:
   ```bash
   resumex tex resume.yaml
   ```

## Custom Themes

`resumex` allows you to go beyond the bundled themes by creating your own.

### Using a local theme

You can point the generator to a folder containing your theme:

```bash
resumex build resume.yaml --theme ./path/to/my-theme
```

### Theme Structure

A theme directory must contain:
- `theme.yaml`: Configuration for allowed sections, templates, and models.
- `templates/main.tex.j2`: The main entry point for the resume layout.
- `partials/`: Reusable Jinja2 fragments for specific sections.

To start a new theme, copy the `default` theme data from the package:
```bash
cp -r src/resumex/themes_data/default ./my-theme
```

## Module Usage

You can also integrate `resumex` into your Python applications:

```python
from pathlib import Path
from resumex.engine.pipeline import build_pdf

result = build_pdf(
    yaml_path=Path("resume.yaml"),
    theme_id="default",  # or a path like "./my-theme"
    out_dir=Path("output")
)

print(f"Resume generated at: {result.pdf_path}")
```

## Development & Testing

We use `uv` for development. To run tests:

```bash
uv run pytest tests/
```

## License

MIT
