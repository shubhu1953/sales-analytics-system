from pathlib import Path

def read_text_lines(file_path):
    return Path(file_path).read_text(encoding="utf-8").splitlines()

def ensure_dir(dir_path):
    p = Path(dir_path)
    p.mkdir(parents=True, exist_ok=True)
    return p

def write_text(file_path, content):
    Path(file_path).write_text(content, encoding="utf-8")
