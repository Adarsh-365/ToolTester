from flask import Flask, render_template, request, redirect, url_for, flash, send_file, jsonify
import os
import shutil

app = Flask(__name__)
app.secret_key = 'dev'

# Target file to edit (mcptool.py in the parent folder)
FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'mcptool.py'))
ALLOWED_FILES = {'mcptool.py': FILE_PATH}

@app.route('/')
def index():
    return redirect(url_for('edit', filename='mcptool.py'))

@app.route('/edit', methods=['GET'])
def edit():
    filename = request.args.get('filename', 'mcptool.py')
    if filename not in ALLOWED_FILES:
        return "File not allowed", 403
    path = ALLOWED_FILES[filename]
    try:
        # Read with newline='' to preserve original line endings exactly
        with open(path, 'r', encoding='utf-8', newline='') as f:
            content = f.read()
    except Exception as e:
        content = f'Error reading file: {e}'
    return render_template('edit.html', filename=filename, content=content)

@app.route('/save', methods=['POST'])
def save():
    filename = request.form.get('filename')
    if filename not in ALLOWED_FILES:
        return "File not allowed", 403
    content = request.form.get('content', '')
    path = ALLOWED_FILES[filename]
    try:
        # Backup the original file before overwriting
        try:
            shutil.copy2(path, path + '.bak')
        except Exception:
            pass

        # Write using newline='' so Python does not alter line endings
        with open(path, 'w', encoding='utf-8', newline='') as f:
            f.write(content)
        flash('Saved successfully. Backup at "' + path + '.bak"', 'success')
    except Exception as e:
        flash(f'Error saving file: {e}', 'error')
    return redirect(url_for('edit', filename=filename))

@app.route('/download')
def download():
    filename = request.args.get('filename', 'mcptool.py')
    if filename not in ALLOWED_FILES:
        return "File not allowed", 403
    return send_file(ALLOWED_FILES[filename], as_attachment=True)
@app.route('/api/chat', methods=['POST'])
def chat_api():
    """Simple chat API that returns a greeting/echo based on question text.

    Expects JSON: {"message": "..."}
    Returns JSON: {"reply": "..."}
    """
    data = request.get_json(silent=True) or {}
    msg = (data.get('message') or '').strip()

    if not msg:
        reply = "Hello! Send me a message and I'll reply."
        return jsonify({'reply': reply})

    low = msg.lower()
    # Simple greeting heuristics
    if any(g in low for g in ('hello', 'hi', 'hey')):
        reply = f"Hello! Nice to meet you — you said: '{msg}'"
    elif '?' in msg:
        reply = f"Good question! Here's a friendly greeting: Hello — regarding your question: '{msg}'"
    else:
        reply = f"You asked: '{msg}'. Hello!"

    return jsonify({'reply': reply})


if __name__ == '__main__':
    # Runs on port 5001 to avoid common conflicts
    app.run(host='127.0.0.1', port=5001, debug=True)
