"""Main CLI entry point for the transpiler."""

import sys
import argparse
from pathlib import Path

from levlang.cli.cli import CLI


def main():
    """Main entry point for the levlang CLI."""
    parser = argparse.ArgumentParser(
        prog='levlang',
        description='LevLang Transpiler - Transpile LevLang to Python/pygame',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Add version argument
    version_text = """
╻  ┏━╸╻ ╻╻  ┏━┓┏┓╻┏━╸
┃  ┣╸ ┃┏┛┃  ┣━┫┃┗┫┃╺┓
┗━╸┗━╸┗┛ ┗━╸╹ ╹╹ ╹┗━┛ 
-----------------------
     Levelium Inc.
-----------------------
>> CLI version 0.1.0
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
        help='Transpile a LevLang file to Python'
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
        help='Watch a LevLang file and automatically retranspile on changes'
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
        help='Transpile and execute a LevLang file'
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
