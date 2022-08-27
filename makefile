.PHONY: install
install:
	@echo "Installing..."
	python -m pip install --upgrade pip
	pip install -r requirements.txt
	@echo "Done."