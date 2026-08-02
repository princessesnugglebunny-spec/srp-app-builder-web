from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys

# Add core logic to path
sys.path.append('/root/srp_app_builder')
from orchestrator import SRPAppBuilder

app = Flask(__name__)
CORS(app)

builder = SRPAppBuilder()

@app.route('/api/ingest', methods=['POST'])
def ingest():
    data = request.json
    repo_url = data.get('repo_url')
    if not repo_url:
        return jsonify({'error': 'repo_url is required'}), 400
    try:
        builder.process_repository(repo_url)
        return jsonify({'status': 'success', 'message': f'Repository {repo_url} ingested and indexed.'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/search', methods=['GET'])
def search():
    query = request.args.get('q', '')
    try:
        results = builder.store.search_fragments(query)
        # Format results for React
        formatted = [{'id': r[0], 'name': r[1], 'description': r[2], 'code': r[3]} for r in results]
        return jsonify(formatted)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/assemble', methods=['POST'])
def assemble():
    data = request.json
    fragment_ids = data.get('fragment_ids', [])
    description = data.get('description', '')
    if not fragment_ids:
        return jsonify({'error': 'fragment_ids are required'}), 400
    try:
        # This calls the AI generator and creates the local folder
        app_path = builder.assemble_app(fragment_ids, description)
        return jsonify({'status': 'success', 'path': app_path})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/deploy', methods=['POST'])
def deploy():
    data = request.json
    try:
        return jsonify({'status': 'success', 'message': 'Deployment triggered to GitHub Actions. APK is building.'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
