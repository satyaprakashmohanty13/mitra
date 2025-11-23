import gradio as gr
import mitra
import args
import os
import shutil
import tempfile

def generate_polyglots(file1, file2, verbose, force, reverse, overlap):
    # Create a temporary directory for this request
    temp_dir = tempfile.mkdtemp()

    # Set context variables for this request
    args.setVar("VERBOSE", verbose)
    args.setVar("FORCE", force)
    args.setVar("REVERSE", reverse)
    args.setVar("OVERLAP", overlap)
    args.setVar("OUTDIR", temp_dir)
    args.setVar("NOFILE", False)
    args.setVar("SPLIT", False)
    args.setVar("SPLITDIR", "")
    args.setVar("PAD", 0)

    # In newer Gradio versions, file inputs are passed as paths (strings), not file objects.
    # We check if it's a string or an object with a .name attribute for compatibility.
    f1_path = file1 if isinstance(file1, str) else file1.name
    f2_path = file2 if isinstance(file2, str) else file2.name

    try:
        mitra.process_files(f1_path, f2_path)
    except Exception as e:
        shutil.rmtree(temp_dir)
        return f"Error: {str(e)}", None

    # Collect generated files
    generated_files = []
    for root, dirs, files in os.walk(temp_dir):
        for file in files:
            generated_files.append(os.path.join(root, file))

    if not generated_files:
        shutil.rmtree(temp_dir)
        return "No polyglots generated.", None

    # Gradio will process the returned file paths.
    # We rely on OS/Gradio to eventually clean up, or valid temporary file usage.
    # Since temp_dir is unique per request, there's no collision.

    return "Polyglots generated successfully!", generated_files

iface = gr.Interface(
    fn=generate_polyglots,
    inputs=[
        gr.File(label="File 1"),
        gr.File(label="File 2"),
        gr.Checkbox(label="Verbose", value=False),
        gr.Checkbox(label="Force (Treat File 2 as binary blob)", value=False),
        gr.Checkbox(label="Reverse (Also try File 2 then File 1)", value=False),
        gr.Checkbox(label="Overlap (Generate overlapping polyglots)", value=False),
    ],
    outputs=[
        gr.Textbox(label="Status"),
        gr.File(label="Generated Polyglots"),
    ],
    title="Mitra Polyglot Generator",
    description="Generate weird files (parasites, polyglots, etc.) using Mitra."
)

if __name__ == "__main__":
    iface.launch()
