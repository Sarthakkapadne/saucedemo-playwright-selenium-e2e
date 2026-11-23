#!/usr/bin/env python3
"""
CLI Test Runner for SauceDemo E2E Test Suite.
Allows running Playwright, Selenium, Smoke, or Regression suites with HTML and Allure reporting.
"""
import argparse
import subprocess
import sys
import os


def main():
    parser = argparse.ArgumentParser(description="SauceDemo E2E Test Runner")
    parser.add_argument(
        "--engine",
        choices=["all", "playwright", "selenium"],
        default="all",
        help="Test execution engine (default: all)",
    )
    parser.add_argument(
        "--suite",
        choices=["all", "smoke", "regression", "e2e"],
        default="all",
        help="Test suite category (default: all)",
    )
    parser.add_argument(
        "--browser",
        choices=["chromium", "firefox", "webkit"],
        default="chromium",
        help="Browser type for Playwright (default: chromium)",
    )
    parser.add_argument(
        "--headed",
        action="store_true",
        help="Run in headed/visible browser mode",
    )
    parser.add_argument(
        "--html-report",
        action="store_true",
        default=True,
        help="Generate standalone HTML test report in reports/report.html",
    )
    parser.add_argument(
        "--allure",
        action="store_true",
        default=True,
        help="Generate Allure report raw results in reports/allure-results",
    )

    args = parser.parse_args()
    os.makedirs("reports", exist_ok=True)

    cmd = [sys.executable, "-m", "pytest", "-v"]

    # Filter markers
    markers = []
    if args.engine != "all":
        markers.append(args.engine)
    if args.suite != "all":
        markers.append(args.suite)

    if markers:
        cmd.extend(["-m", " and ".join(markers)])

    # Browser options
    cmd.extend(["--browser-name", args.browser])
    cmd.extend(["--headless-mode", "false" if args.headed else "true"])

    if args.html_report:
        cmd.extend(["--html=reports/report.html", "--self-contained-html"])

    if args.allure:
        cmd.extend(["--alluredir=reports/allure-results"])

    print("=" * 70)
    print("🚀 SauceDemo E2E Automation Suite")
    print(f"   Engine: {args.engine} | Suite: {args.suite} | Browser: {args.browser}")
    print(f"   Command: {' '.join(cmd)}")
    print("=" * 70)

    result = subprocess.run(cmd)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
