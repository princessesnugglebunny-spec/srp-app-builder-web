import os
import sys
from pathlib import Path
from srp_app_builder.store.index import IndexedStore
from srp_app_builder.generator.assembler import AIAppGenerator

def deploy_to_apk(selected_ids, app_description, repo_owner, repo_name, github_mcp):
    print(f"🚀 Starting One-Click Deployment for: {app_description}")
    build_path = Path("/root/srp_apps/cloud_build")
    store = IndexedStore()
    gen = AIAppGenerator(store)
    package_path = gen.create_app_package(selected_ids, app_description, str(build_path))
    files_to_push = []
    for root, _, files in os.walk(build_path):
        for file in files:
            full_path = Path(root) / file
            relative_path = full_path.relative_to(build_path)
            with open(full_path, "r", encoding="utf-8") as f:
                files_to_push.append({"path": str(relative_path), "content": f.read()})
    github_mcp.push_files(owner=repo_owner, repo=repo_name, branch="main", files=files_to_push, message=f"Deploying assembled app: {app_description}")
    print("✅ Files pushed to GitHub. APK is building.")
