"""Main CLI entry point for the transpiler."""

import sys
import argparse
from pathlib import Path

from gamelang.cli.cli import CLI


def main():
    """Main entry point for the gamelang CLI."""
    parser = argparse.ArgumentParser(
        prog='gamelang',
        description='Game Language Transpiler - Transpile game language to Python/pygame',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Add version argument
    parser.add_argument(
        '--version',
        action='version',
        version='GameLang Transpiler v0.1.0'
    )
    
    # Create subparsers for commands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Transpile command
    transpile_parser = subparsers.add_parser(
        'transpile',
        help='Transpile a game language file to Python'
    )
    transpile_parser.add_argument(
        'input',
        type=str,
        help='Input game language file (.game)'
    )
    transpile_parser.add_argument(
        '-o', '--output',
        type=str,
        help='Output Python file (.py). If not specified, uses input filename with .py extension'
    )
    
    # Watch command
    watch_parser = subparsers.add_parser(
        'watch',
        help='Watch a game language file and automatically retranspile on changes'
    )
    watch_parser.add_argument(
        'input',
        type=str,
        help='Input game language file (.game) to watch'
    )
    watch_parser.add_argument(
        '-o', '--output',
        type=str,
        help='Output Python file (.py). If not specified, uses input filename with .py extension'
    )
    
    # Run command
    run_parser = subparsers.add_parser(
        'run',
        help='Transpile and execute a game language file'
    )
    run_parser.add_argument(
        'input',
        type=str,
        help='Input game language file (.game) to run'
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
