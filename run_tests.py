#!/usr/bin/env python
"""
Main Test Runner & Interactive AI-QA Demonstration CLI.

Usage:
  python run_tests.py --suite all
  python run_tests.py --suite api
  python run_tests.py --suite ui
  python run_tests.py --suite ai
  python run_tests.py --demo-ai
"""

import argparse
import subprocess
import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


def run_pytest_suite(suite_name: str, generate_html: bool = True) -> int:
    """Execute pytest with appropriate filter arguments."""
    cmd = [sys.executable, "-m", "pytest"]

    if suite_name == "api":
        cmd.extend(["-m", "api"])
    elif suite_name == "ui":
        cmd.extend(["-m", "ui"])
    elif suite_name == "ai":
        cmd.extend(["-m", "ai"])
    elif suite_name == "smoke":
        cmd.extend(["-m", "smoke"])
    elif suite_name == "self_healing":
        cmd.extend(["-m", "self_healing"])

    if generate_html:
        report_path = Path("reports/report.html")
        report_path.parent.mkdir(parents=True, exist_ok=True)
        cmd.extend([f"--html={report_path}", "--self-contained-html"])

    console.print(Panel(f"[bold cyan]Executing AI-QA-Suite Test Runner[/bold cyan]\nCommand: `{' '.join(cmd)}`", border_style="cyan"))
    return subprocess.run(cmd).returncode


def interactive_ai_demo():
    """Run an interactive demonstration of all 5 AI capabilities without external paid APIs."""
    console.print(Panel("[bold green]AI-QA-Suite: Interactive AI Capability Showcase (Zero-Cost Local Mode)[/bold green]", border_style="green"))

    from ai.test_case_generator import TestCaseGenerator
    from ai.bug_analyzer import BugAnalyzer
    from ai.log_analyzer import LogAnalyzer
    from ai.test_data_generator import TestDataGenerator
    from ai.providers import MockAIProvider
    from utils.test_data import TestDataManager

    provider = MockAIProvider()
    test_data = TestDataManager()

    # 1. AI Test Case Generator
    console.print("\n[bold yellow]1. AI-Assisted Test Case Generation[/bold yellow]")
    req = test_data.load_json("sample_requirements.json")["requirements"][0]
    gen = TestCaseGenerator(provider)
    tc_result = gen.generate_from_requirement(req["text"], req["module"])

    table = Table(title=f"Generated Test Cases: {tc_result['feature']}", show_lines=True)
    table.add_column("ID", style="cyan", width=12)
    table.add_column("Title", style="white")
    table.add_column("Type", style="magenta", width=10)
    table.add_column("Priority", style="red", width=8)

    for tc in tc_result["test_cases"]:
        table.add_row(tc["test_case_id"], tc["title"], tc["type"], tc["priority"])
    console.print(table)

    # 2. AI Bug Analyzer
    console.print("\n[bold yellow]2. AI Bug & Root Cause Analyzer[/bold yellow]")
    bug = test_data.load_json("sample_requirements.json")["sample_bugs"][0]
    analyzer = BugAnalyzer(provider)
    bug_result = analyzer.analyze_bug(bug["title"], bug["description"], bug["error_message"], bug["stack_trace"])

    console.print(f"[bold]Probable Category:[/bold] {bug_result['probable_category']}")
    console.print(f"[bold]Root Cause:[/bold] {bug_result['probable_root_cause']}")
    console.print(f"[bold]Suggested Priority:[/bold] [red]{bug_result['suggested_priority']}[/red]")

    # 3. AI Log Analyzer
    console.print("\n[bold yellow]3. AI Log Stream Analyzer[/bold yellow]")
    logs = test_data.load_text("sample_logs.txt")
    log_an = LogAnalyzer(provider)
    log_res = log_an.analyze_logs(logs)

    console.print(f"[bold]Log Summary:[/bold] {log_res['summary']}")
    console.print(f"[bold]Root Cause:[/bold] {log_res['probable_root_cause']}")
    console.print(f"[bold]Next Debugging Steps:[/bold] {log_res['suggested_next_debugging_steps']}")

    # 4. AI Test Data Generation
    console.print("\n[bold yellow]4. AI Synthetic Test Data Generation[/bold yellow]")
    data_gen = TestDataGenerator(provider)
    data_res = data_gen.generate_dataset("User Accounts")
    console.print(f"Synthesized {data_res['total_records']} structured test records.")

    console.print(Panel("[bold green]All AI QA Capabilities Demonstrated Successfully![/bold green]", border_style="green"))


def main():
    parser = argparse.ArgumentParser(description="AI-QA-Suite Test Execution & Demo CLI")
    parser.add_argument(
        "--suite",
        choices=["all", "api", "ui", "ai", "smoke", "self_healing"],
        default="all",
        help="Test suite group to execute",
    )
    parser.add_argument("--demo-ai", action="store_true", help="Run interactive AI capability showcase")
    parser.add_argument("--no-html", action="store_true", help="Skip HTML report generation")

    args = parser.parse_args()

    if args.demo_ai:
        interactive_ai_demo()
        return 0

    return run_pytest_suite(args.suite, generate_html=not args.no_html)


if __name__ == "__main__":
    sys.exit(main())
