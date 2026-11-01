import argparse
import logging
import sys
import pathlib
import chardet

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_argparse():
    """
    Sets up the argument parser for the command-line interface.
    """
    parser = argparse.ArgumentParser(description="Detects the character encoding of a text file.")
    parser.add_argument("file_path", type=str, help="Path to the file to analyze.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging (DEBUG level).")
    return parser

def detect_encoding(file_path):
    """
    Detects the character encoding of a file.

    Args:
        file_path (str): The path to the file.

    Returns:
        str: The detected encoding, or None if detection fails.
    """
    try:
        # Input Validation: Check if the file path is valid.
        file_path_obj = pathlib.Path(file_path)
        if not file_path_obj.exists():
            logging.error(f"File not found: {file_path}")
            return None
        if not file_path_obj.is_file():
            logging.error(f"Not a file: {file_path}")
            return None

        with open(file_path, 'rb') as f:
            # The whole file goes to chardet at once. Detection on a prefix would
            # be cheaper, but chardet's answer can change as more bytes arrive, and
            # I would rather report the whole file's encoding than its first block's.
            raw_data = f.read()

        # Use chardet to detect the encoding
        result = chardet.detect(raw_data)
        encoding = result['encoding']
        confidence = result['confidence']

        if encoding:
        # Confidence is logged and then ignored. A low confidence guess is
        # returned exactly like a certain one, so the printed answer carries no
        # hint of how much to trust it. Callers who need the confidence have to
        # read the log line, not the result.
            logging.info(f"Detected encoding: {encoding} with confidence: {confidence}")
            return encoding
        else:
            logging.warning("Encoding detection failed.")
            return None

    except Exception as e:
        logging.error(f"An error occurred during encoding detection: {e}")
        return None


# Every failure in detect_encoding collapses to None: missing file, not
# a file, unreadable, and chardet having no answer are indistinguishable
# from here, and all of them print the same failure line and exit 1.
def main():
    """
    Main function to parse arguments, detect encoding, and print the result.
    """
    parser = setup_argparse()
    args = parser.parse_args()

    # Configure verbose logging if specified
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug("Verbose logging enabled.")

    file_path = args.file_path

    encoding = detect_encoding(file_path)

    if encoding:
        print(f"Encoding: {encoding}")
        sys.exit(0)
    else:
        print("Encoding detection failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()

# Usage Examples:
# 1. Detect encoding of a file: python file_encoding_detector.py my_file.txt
# 2. Detect encoding with verbose logging: python file_encoding_detector.py my_file.txt -v