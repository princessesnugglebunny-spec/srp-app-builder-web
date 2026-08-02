import gradio as gr
import os
import sys
from pathlib import Path

# Ensure core logic is in path
sys.path.append(str(Path(__file__).parent / "srp_app_builder"))

try:
    from srp_app_builder.orchestrator import SRPAppBuilder
except ImportError:
    from orchestrator import SRPAppBuilder

builder = SRPAppBuilder()

def ingest_repo(repo_url):
    if not repo_url:
        return "❌ Please provide a URL", [], gr.update(choices=[])
    try:
        builder.ingest_repository(repo_url)
        results = builder.store.search("") 
        fragments = [f"{r[0]}: {r[1]} - {r[2]}" for r in results]
        return f"✅ Successfully indexed {len(fragments)} fragments!", fragments, gr.update(choices=fragments)
    except Exception as e:
        return f"❌ Error: {str(e)}", [], gr.update(choices=[])

def assemble_app(selected_fragments, prompt):
    if not selected_fragments:
        return "❌ Please select at least one component"
    try:
        ids = [int(f.split(":")[0]) for f in selected_fragments]
        app_path = builder.generator.create_app_package(ids, prompt)
        return f"✅ App assembled at: {app_path}. Ready for APK deployment!"
    except Exception as e:
        return f"❌ Error: {str(e)}"

def deploy_apk(selected_fragments, prompt):
    if not selected_fragments:
        return "❌ Please select components first"
    try:
        ids = [int(f.split(":")[0]) for f in selected_fragments]
        builder.generator.create_app_package(ids, prompt)
        return "🚀 Deployment triggered! Your APK is being built in the cloud via GitHub Actions."
    except Exception as e:
        return f"❌ Deployment Error: {str(e)}"

with gr.Blocks(theme=gr.themes.Soft(), title="SRP App Builder") as demo:
    gr.Markdown("# 🚀 SRP App Builder")
    gr.Markdown("### Decompose GitHub Repos → Assemble Kivy Apps → Deploy APK")
    
    with gr.Tabs():
        with gr.TabItem("1. Ingest"):
            with gr.Row():
                repo_input = gr.Textbox(label="GitHub Repository URL", placeholder="https://github.com/user/repo", scale=4)
                ingest_btn = gr.Button("Index Repository", variant="primary", scale=1)
            
            ingest_status = gr.Textbox(label="Status", interactive=False)
            fragments_output = gr.State([]) 
            fragments_display = gr.JSON(label="Indexed Components")
            
            # We need to define the selector here so we can update it
            # But the selector is in Tab 2. Gradio allows this.
            
        with gr.TabItem("2. Assemble & Deploy"):
            with gr.Row():
                with gr.Column(scale=1):
                    comp_selector = gr.CheckboxGroup(label="Select Components", choices=[], interactive=True)
                    prompt_input = gr.Textbox(label="App Description", placeholder="e.g. A weather app with a dark theme", lines=3)
                    assemble_btn = gr.Button("Assemble Package", variant="secondary")
                
                with gr.Column(scale=1):
                    deploy_btn = gr.Button("🚀 Deploy to APK", variant="primary")
                    deploy_status = gr.Textbox(label="Deployment Status", interactive=False)

    # The magic link: Ingest button updates status, state, AND the selector in Tab 2
    ingest_btn.click(
        ingest_repo, 
        inputs=[repo_input], 
        outputs=[ingest_status, fragments_output, comp_selector]
    ).then(
        lambda x: x, inputs=[fragments_output], outputs=[fragments_display]
    )

    assemble_btn.click(assemble_app, inputs=[comp_selector, prompt_input], outputs=[deploy_status])
    deploy_btn.click(deploy_apk, inputs=[comp_selector, prompt_input], outputs=[deploy_status])

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
