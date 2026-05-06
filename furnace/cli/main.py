from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from furnace.cli.evaluate import evaluate_study
from furnace.cli.optimize import optimize_study
from furnace.cli.profile import profile_study
from furnace.cli.report import report_path
from furnace.cli.run import run_study

app = typer.Typer(help="Furnace CLI")
console = Console()


@app.command()
def run(config: Path = typer.Option(..., exists=True, dir_okay=False)) -> None:
    output_dir = run_study(config)
    console.print(f"Study completed. Outputs: [bold]{output_dir}[/bold]")


@app.command()
def profile(config: Path = typer.Option(..., exists=True, dir_okay=False)) -> None:
    output_dir = profile_study(config)
    console.print(f"Profile completed. Outputs: [bold]{output_dir}[/bold]")


@app.command()
def optimize(config: Path = typer.Option(..., exists=True, dir_okay=False)) -> None:
    output_dir = optimize_study(config)
    console.print(f"Optimization completed. Outputs: [bold]{output_dir}[/bold]")


@app.command()
def evaluate(config: Path = typer.Option(..., exists=True, dir_okay=False)) -> None:
    output_dir = evaluate_study(config)
    console.print(f"Evaluation completed. Outputs: [bold]{output_dir}[/bold]")


@app.command()
def report(run_dir: Path = typer.Option(..., exists=True, file_okay=False)) -> None:
    console.print(f"Report: [bold]{report_path(run_dir)}[/bold]")
