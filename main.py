import sys
from pathlib import Path

# Add src to sys.path to allow importing resumex without installation
src_path = Path(__file__).parent / "src"
sys.path.append(str(src_path))

from resumex.cli import app

if __name__ == "__main__":
    app()
