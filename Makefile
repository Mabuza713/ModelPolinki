CreateVenv_windows:
	python3 -m venv .env
	.\.env\Scripts\activate.bat

CreateVenv_linux:
	python3 -m venv .env
	source ./.env/Scripts/activate

UpgradePIP:
	python -m pip install --upgrade pip

InstallDepend_windows:
	.env\Scripts\pip3 install -r Requirements.txt