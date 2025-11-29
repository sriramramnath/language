"""Main CLI entry point for the transpiler."""

import sys
import argparse
from pathlib import Path

from levlang.cli.cli import CLI


def main():
    """Main entry point for the levlang CLI."""
    parser = argparse.ArgumentParser(
        prog='levlang',
        description='LevLang Transpiler - A simple, declarative language for creating pygame games',
        epilog='''
Examples:
  levlang transpile game.lvl              # Transpile to game.py
  levlang transpile game.lvl -o output.py # Specify output file
  levlang run game.lvl                     # Transpile and run
  levlang watch game.lvl                   # Watch for changes and retranspile

Documentation: https://github.com/yourusername/levlang
Error Codes: See docs/ERROR_CODES.md
        ''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Add version argument with colors
    C = '\033[96m'  # Bright Cyan
    G = '\033[92m'  # Bright Green
    W = '\033[97m'  # Bright White
    D = '\033[2m'   # Dim
    R = '\033[0m'   # Reset
    
    version_text = f"""
{C} ╻  ┏━╸╻ ╻╻  ┏━┓┏┓╻┏━╸{R}
{C} ┃  ┣╸ ┃┏┛┃  ┣━┫┃┗┫┃╺┓{R}
{C} ┗━╸┗━╸┗┛ ┗━╸╹ ╹╹ ╹┗━┛{R}
{D}-----------------------{R}
{W}    Levelium Inc.{R}
{D}-----------------------{R}
{G}>> CLI version 0.3.3{R}
"""
    parser.add_argument(
        '--version',
        action='version',
        version=version_text
    )
    
    # Create subparsers for commands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Transpile command
    transpile_parser = subparsers.add_parser(
        'transpile',
        help='Transpile a LevLang file to Python',
        description='Convert a .lvl file to executable Python code'
    )
    transpile_parser.add_argument(
        'input',
        type=str,
        help='Input LevLang file (.lvl)'
    )
    transpile_parser.add_argument(
        '-o', '--output',
        type=str,
        help='Output Python file (.py). If not specified, uses input filename with .py extension'
    )
    
    # Watch command
    watch_parser = subparsers.add_parser(
        'watch',
        help='Watch a LevLang file and automatically retranspile on changes',
        description='Monitor a .lvl file and automatically retranspile when it changes. Press Ctrl+C to stop.'
    )
    watch_parser.add_argument(
        'input',
        type=str,
        help='Input LevLang file (.lvl) to watch'
    )
    watch_parser.add_argument(
        '-o', '--output',
        type=str,
        help='Output Python file (.py). If not specified, uses input filename with .py extension'
    )
    
    # Run command
    run_parser = subparsers.add_parser(
        'run',
        help='Transpile and execute a LevLang file',
        description='Transpile a .lvl file and immediately run the generated Python code. Supports level chaining via __NEXT_LEVEL__ markers.'
    )
    run_parser.add_argument(
        'input',
        type=str,
        help='Input LevLang file (.lvl) to run'
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # If no command specified, show help
    if not args.command:
        parser.print_help()
        return 0
    
    # Create CLI instance and execute command
    cli = CLI()
    
    try:
        if args.command == 'transpile':
            return cli.transpile_file(args.input, args.output)
        elif args.command == 'watch':
            return cli.watch_mode(args.input, args.output)
        elif args.command == 'run':
            return cli.run_file(args.input)
        else:
            parser.print_help()
            return 1
    except KeyboardInterrupt:
        print("\nInterrupted by user")
        return 130
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
