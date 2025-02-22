#!/usr/bin/env bash

# Exit on error
set -e

# Define package directory
PACKAGE_DIR=$(pwd)

# Install uv if not already installed
if ! command -v uv &> /dev/null; then
    echo "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    # Add uv to PATH for this session
    export PATH="$HOME/.cargo/bin:$PATH"
fi

# Create and set up virtual environment with uv
echo "Creating virtual environment..."
uv venv "$PACKAGE_DIR/.venv"

# Install the package into the venv using uv
echo "Installing package dependencies..."
uv pip install "$PACKAGE_DIR"

# Create ~/bin if it doesn’t exist
mkdir -p ~/bin

# Create download_docs script with proper variable expansion
echo "Setting up download_docs script..."
cat > ~/bin/download_docs << EOF
#!/usr/bin/env bash
PACKAGE_DIR=$PACKAGE_DIR
source "\$PACKAGE_DIR/.venv/bin/activate"
python "\$PACKAGE_DIR/mdCrawler/cli.py" "\$@"
EOF
chmod +x ~/bin/download_docs

# Add ~/bin to PATH in .zshrc if not already present
if ! grep -q "$HOME/bin" ~/.zshrc; then
    echo "Updating .zshrc with ~/bin in PATH..."
    echo "if [ -d \"\$HOME/bin\" ]; then export PATH=\"\$HOME/bin:\$PATH\"; fi" >> ~/.zshrc
fi

echo "Installation complete! Run \"source ~/.zshrc\" and then use \"download_docs\" from anywhere."