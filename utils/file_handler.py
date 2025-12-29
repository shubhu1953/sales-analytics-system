from pathlib import Path

def read_text_lines(file_path):
    return Path(file_path).read_text(encoding="utf-8").splitlines()

def ensure_dir(dir_path):
    p = Path(dir_path)
    p.mkdir(parents=True, exist_ok=True)
    return p

def write_text(file_path, content):
    Path(file_path).write_text(content, encoding="utf-8")

def read_sales_data(filename):
    """
    Reads sales data from file handling encoding issues.
    Returns: list of raw lines (strings), excluding header
    """
    encodings = ["utf-8", "latin-1", "cp1252"]

    for enc in encodings:
        try:
            with open(filename, "r", encoding=enc) as f:
                lines = f.readlines()
                return [line.strip() for line in lines[1:] if line.strip()]
        except UnicodeDecodeError:
            continue
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {filename}")

    raise UnicodeDecodeError("Unable to decode file with supported encodings")

