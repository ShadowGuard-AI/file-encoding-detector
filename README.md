![Banner](banner.png)

# file-encoding-detector
Detects the character encoding of a text file (e.g., UTF-8, ASCII, Latin-1) and outputs it. Uses heuristics and library-based detection. - Focused on File operations and analysis

## Install
`git clone https://github.com/ShadowStrikeHQ/file-encoding-detector`

## Usage
`./file-encoding-detector [params]`

## Parameters
- `-h`: Show help message and exit
- `-v`: Enable verbose logging (DEBUG level).

## Exit codes
- `0`: an encoding was detected and printed.
- `1`: detection failed. This covers a missing file, a path that is not a file (for example a directory), an empty file, and a sample whose encoding cannot be detected. Each failure prints its failure line and exits 1.

## License
Copyright (c) ShadowStrikeHQ
