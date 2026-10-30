"""Tiny notes viewer: reads a note by name from a notes directory."""
import tempfile
from pathlib import Path

MAX_BYTES = 100_000


def read_note(notes_dir: Path, name: str) -> str:
    if not isinstance(name, str) or not name or "\x00" in name:
        raise ValueError("invalid note name")

    base = notes_dir.resolve()
    path = (base / name).resolve()
    if not path.is_relative_to(base):
        raise PermissionError("access outside the notes directory is not allowed")

    if not path.is_file() or path.stat().st_size > MAX_BYTES:
        raise FileNotFoundError("note not found")
    return path.read_text(encoding="utf-8")


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "notes").mkdir()
        (root / "notes" / "hello.txt").write_text("Welcome to the notes viewer.\n", encoding="utf-8")
        (root / "secret.txt").write_text("API_KEY=do-not-share\n", encoding="utf-8")
        names = [
            "hello.txt",
            "../secret.txt",
            str(root / "secret.txt"),
            "missing.txt",
        ]
        for name in names:
            try:
                print(f"{name!r}: {read_note(root / 'notes', name).strip()}")
            except (ValueError, FileNotFoundError) as error:
                print(f"{name!r}: error - {error}")


if __name__ == "__main__":
    main()