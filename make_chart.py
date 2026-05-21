"""Render a bar chart comparing BLAS backends across systems.

Data is parsed from the summary table in README.md so the README is the single
source of truth. Run with:

    pixi run chart
"""

from __future__ import annotations

import re
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

README_PATH = Path(__file__).with_name("README.md")
OUTPUT_PATH = Path(__file__).with_name("chart.png")

BACKEND_COLORS = {
    "OpenBLAS":   "#4C78A8",
    "MKL":        "#F58518",
    "Accelerate": "#54A24B",
    "BLIS":       "#E45756",
}


def _strip_cell(cell: str) -> str:
    """Strip whitespace and markdown bold markers from a table cell."""
    return cell.strip().strip("*").strip()


def _parse_time(cell: str) -> float:
    """Parse a time cell like '**4.30s**' or '5.14s' into a float (seconds)."""
    text = _strip_cell(cell)
    match = re.match(r"([\d.]+)\s*s?$", text)
    if not match:
        raise ValueError(f"Could not parse time from cell: {cell!r}")
    return float(match.group(1))


def _split_row(line: str) -> list[str]:
    stripped = line.strip()
    if stripped.startswith("|"):
        stripped = stripped[1:]
    if stripped.endswith("|"):
        stripped = stripped[:-1]
    return stripped.split("|")


def parse_summary_table(
    markdown: str,
) -> tuple[list[str], list[tuple[str, str, list[float]]]]:
    """Return (operation_names, rows) from the first markdown table in *markdown*."""
    table_lines: list[str] = []
    in_table = False
    for line in markdown.splitlines():
        if line.lstrip().startswith("|"):
            table_lines.append(line)
            in_table = True
        elif in_table:
            break

    if len(table_lines) < 3:
        raise ValueError("No markdown table with header/separator/data rows found.")

    header = [_strip_cell(c) for c in _split_row(table_lines[0])]
    operation_names = header[2:]  # columns after "System" and "Backend"

    rows: list[tuple[str, str, list[float]]] = []
    for line in table_lines[2:]:  # skip header + separator
        cells = _split_row(line)
        if len(cells) != len(header):
            continue
        system = _strip_cell(cells[0])
        backend = _strip_cell(cells[1])
        times = [_parse_time(c) for c in cells[2:]]
        rows.append((system, backend, times))

    return operation_names, rows


def _shorten_system(name: str) -> str:
    """Make system labels a bit more compact for the chart axis."""
    return name.replace(" cores ", "c ")


def render(operations: list[str], rows: list[tuple[str, str, list[float]]]) -> None:
    labels = [f"{_shorten_system(sys)}  [{be}]" for sys, be, _ in rows]
    colors = [BACKEND_COLORS.get(be, "#888888") for _, be, _ in rows]
    values = np.array([row for _, _, row in rows], dtype=float)

    fig, axes = plt.subplots(1, len(operations), figsize=(20, 6), sharey=True)
    y_positions = np.arange(len(labels))

    for ax, op_idx, op_name in zip(axes, range(len(operations)), operations):
        times = values[:, op_idx]
        best = times.min()
        bars = ax.barh(y_positions, times, color=colors, edgecolor="black", linewidth=0.4)

        # Highlight the best (shortest) bar.
        for i, bar in enumerate(bars):
            if times[i] == best:
                bar.set_edgecolor("black")
                bar.set_linewidth(1.8)

        for i, t in enumerate(times):
            ax.text(t, i, f" {t:.2f}s", va="center", ha="left", fontsize=8)

        ax.set_title(op_name, fontsize=11)
        ax.set_xlabel("seconds (lower is better)")
        ax.invert_yaxis()
        ax.set_xlim(0, times.max() * 1.18)
        ax.grid(axis="x", linestyle=":", alpha=0.5)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    axes[0].set_yticks(y_positions)
    axes[0].set_yticklabels(labels, fontsize=9)

    backends_present = {be for _, be, _ in rows}
    legend_handles = [
        plt.Rectangle((0, 0), 1, 1, color=color, label=backend)
        for backend, color in BACKEND_COLORS.items()
        if backend in backends_present
    ]
    fig.legend(
        handles=legend_handles,
        loc="upper center",
        ncol=len(legend_handles),
        bbox_to_anchor=(0.5, 1.02),
        frameon=False,
        fontsize=10,
    )

    fig.suptitle("NumPy linear algebra: BLAS backend comparison", y=1.06, fontsize=13)
    fig.tight_layout()
    fig.savefig(OUTPUT_PATH, dpi=150, bbox_inches="tight")
    print(f"Wrote {OUTPUT_PATH}")


def main() -> None:
    markdown = README_PATH.read_text(encoding="utf-8")
    operations, rows = parse_summary_table(markdown)
    render(operations, rows)


if __name__ == "__main__":
    main()

