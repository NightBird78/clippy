#!/usr/bin/env python3
import sys
import subprocess
import argparse
import os
import shutil

def copy_to_clipboard(content, verbose=False):
    try:
        subprocess.run(['xclip', '-selection', 'clipboard'], input=content.encode('utf-8'), check=True)
        if verbose:
            print(f"Copied to clipboard (via xclip): {content[:50]}{'...' if len(content) > 50 else ''}")
    except subprocess.CalledProcessError as e:
        print(f"Error copying to clipboard: {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print("Error: No 'xclip' is installed. Install with 'sudo apt install xclip'", file=sys.stderr)
        sys.exit(1)

def paste_from_clipboard(output_file, index=0, verbose=False, overwrite=False):
    if index < 0:
        print("Error: Index must be non-negative", file=sys.stderr)
        sys.exit(1)
    try:
        if shutil.which('copyq'):
            process = subprocess.run(['copyq', 'read', str(index)], capture_output=True, text=True, check=True)
            content = process.stdout
            if not content:
                print(f"Error: No content found at CopyQ history index {index}", file=sys.stderr)
                sys.exit(1)
        else:
            if index != 0:
                print("Error: History index requires CopyQ. Install with 'sudo apt install copyq'", file=sys.stderr)
                sys.exit(1)
            process = subprocess.run(['xclip', '-selection', 'clipboard', '-o'], capture_output=True, text=True, check=True)
            content = process.stdout

        mode = 'w' if overwrite else 'a'
        with open(output_file, mode, encoding='utf-8') as f:
            f.write(content)
        if verbose:
            action = "Overwritten" if overwrite else "Appended"
            suffix = f" (CopyQ history index {index})" if shutil.which('copyq') and index != 0 else ''
            print(f"{action} clipboard content to: {output_file}{suffix}")
    except subprocess.CalledProcessError as e:
        print(f"Error pasting from clipboard: {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print("Error: Neither 'copyq' nor 'xclip' is installed. Install with 'sudo apt install copyq' or 'sudo apt install xclip'", file=sys.stderr)
        sys.exit(1)
    except IOError as e:
        print(f"Error writing to file {output_file}: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="clippy: A simple clipboard tool for Ubuntu with CopyQ integration",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""Examples:
  Copy file path(s) to clipboard:
      clippy file1.txt file2.txt

  Copy file content as text:
      clippy -t file.txt

  Paste current clipboard to a file (append by default):
      clippy --paste output.txt

  Paste the 2nd item from CopyQ history to a file, overwriting:
      clippy --paste -i 1 -w output.txt

  Copy piped input to clipboard:
      curl https://jsonplaceholder.typicode.com/users | clippy
"""
    )
    parser.add_argument('files', nargs='*', help="Files to copy as paths or paste to (with --paste)")
    parser.add_argument('-v', '--verbose', action='store_true', help="Show verbose output")
    parser.add_argument('-t', '--text', action='store_true', help="Copy file content as text instead of path")
    parser.add_argument('--paste', action='store_true', help="Paste clipboard content to the specified file")
    parser.add_argument('-i', '--index', type=int, default=0, help="CopyQ history index to paste (0 for current, 1 for previous, etc.)")
    parser.add_argument('-w', '--write', action='store_true', help="Overwrite the output file instead of appending")

    # Normalize shorthands like -1, -2 into --index
    raw_args = []
    for arg in sys.argv[1:]:
        if arg.startswith('-') and len(arg) > 1 and arg[1:].isdigit():
            raw_args.extend(['--index', arg[1:]])
        else:
            raw_args.append(arg)

    args = parser.parse_args(raw_args)

    if args.paste:
        if not args.files:
            print("Error: --paste requires a file to write to", file=sys.stderr)
            sys.exit(1)
        if len(args.files) > 1:
            print("Error: --paste supports only one output file", file=sys.stderr)
            sys.exit(1)
        paste_from_clipboard(args.files[0], args.index, args.verbose, args.write)
        return

    if not sys.stdin.isatty():
        content = sys.stdin.read()
        if content:
            copy_to_clipboard(content, args.verbose)
        else:
            print("No piped input provided", file=sys.stderr)
            sys.exit(1)
    elif args.files:
        if args.text:
            try:
                with open(args.files[0], 'r', encoding='utf-8') as f:
                    content = f.read()
                    copy_to_clipboard(content, args.verbose)
            except (IOError, UnicodeDecodeError) as e:
                print(f"Error reading file {args.files[0]}: {e}", file=sys.stderr)
                sys.exit(1)
        else:
            content = '\n'.join(os.path.abspath(f) for f in args.files)
            copy_to_clipboard(content, args.verbose)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()

