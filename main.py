#!/usr/bin/env python3
"""
Multi-Agent Meal Planning System - Entry Point

Run this file to start the interactive meal planner.
For a quick demo without setup, run: python simulate.py
"""
import sys
import subprocess
import argparse
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root (if present)
project_root = Path(__file__).resolve().parent
load_dotenv(project_root / ".env")

def run_subprocess(script_path: str, args=None) -> int:
    args = args or []
    cmd = [sys.executable, str(script_path)] + args
    try:
        res = subprocess.run(cmd, check=False)
        return res.returncode
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
        return 130
    except Exception as e:
        print(f"Failed to run {script_path}: {e}")
        return 1

def main():
    parser = argparse.ArgumentParser(description="Multi-Agent Meal Planning System launcher")
    parser.add_argument("--demo", action="store_true", help="Run quick demo (simulate.py)")
    parser.add_argument("--interactive", action="store_true", help="Start interactive CLI (src/main.py)")
    args = parser.parse_args()

    if args.demo:
        print("\n🚀 Running quick demo...\n")
        rc = run_subprocess(project_root / "simulate.py")
        sys.exit(rc)

    if args.interactive:
        print("\n🚀 Starting interactive CLI...\n")
        rc = run_subprocess(project_root / "src" / "main.py")
        sys.exit(rc)

    # If no flag given, show choice menu
    print("=" * 60)
    print("  Multi-Agent Meal Planning System")
    print("=" * 60)
    print()
    print("Choose how to run:")
    print("  1. Interactive CLI (full experience)")
    print("  2. Quick Demo (no setup needed)")
    print()

    try:
        choice = input("Enter choice (1 or 2): ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\nExiting.")
        sys.exit(0)

    if choice == "2":
        print("\n🚀 Running quick demo...\n")
        rc = run_subprocess(project_root / "simulate.py")
    else:
        print("\n🚀 Starting interactive CLI...\n")
        rc = run_subprocess(project_root / "src" / "main.py")

    sys.exit(rc)

if __name__ == "__main__":
    main()