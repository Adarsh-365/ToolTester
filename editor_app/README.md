# Simple Flask File Editor

This small Flask app provides a web UI to edit and save `Main.py` located in the project root (`..\Main.py`).

Usage:

1. Create a virtual environment and install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Run the app from `d:\DL\ToolTester`:

```powershell
python editor_app\app.py
```

3. Open `http://127.0.0.1:5001/` in your browser. You can edit and save `Main.py` from the web UI.

Security note: This example intentionally restricts editing to `Main.py` only. Do not expose this app to untrusted networks.
