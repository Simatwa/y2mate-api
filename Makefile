# Define targets
.PHONY: install build clean

# Define variables
PYTHON := python3
PI := $(PYTHON) -m pip
BUILD_NAME := y2mate



# Default target
default: install

# Target to install 
install:
	$(PI) install .

# Target to create an executable using PyInstaller
build: install
	$(PI) install --upgrade pyinstaller
	$(PYTHON) -m PyInstaller main.py --onefile --exclude pandas --distpath dist --workpath build --log-level INFO --exclude numpy --exclude matplotlib --exclude PyQt5 --exclude PyQt6 --exclude share --icon assets/logo.png --contents-directory .  --noconfirm --name $(BUILD_NAME)

# Target to clean up build artifacts
clean:
	rm -rf build/ dist/ *.spec *.deb
