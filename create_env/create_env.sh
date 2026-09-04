SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

python -m venv .env

if [ -f .env/bin/activate ]; then
  source .env/bin/activate
else
  source .env/Scripts/activate
fi

pip3 install -r "$SCRIPT_DIR/requirements.txt"