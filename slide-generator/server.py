from flask import Flask, request, send_file
import subprocess
import os
import uuid
import traceback  # Import this to print detailed error logs

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate_slides():
    input_filename = None
    output_filename = None

    try:
        data = request.json
        if not data:
            return {"error": "Invalid JSON body"}, 400
            
        markdown_content = data.get('markdown')
        if not markdown_content:
            return {"error": "No 'markdown' field provided"}, 400

        # Create unique filenames
        run_id = str(uuid.uuid4())
        input_filename = f"slides_{run_id}.md"
        output_filename = f"slides_{run_id}.pdf"

        # Write Markdown file
        with open(input_filename, 'w') as f:
            f.write(markdown_content)

        # Run Marp
        # We explicitly rely on the global install from the Dockerfile
        cmd = [
            "marp", 
            input_filename, 
            "--pdf", 
            "--output", output_filename, 
            "--allow-local-files"
        ]
        
        print(f"Executing: {' '.join(cmd)}") # Print to Docker logs
        
        subprocess.run(cmd, check=True, capture_output=True, text=True)

        return send_file(output_filename, as_attachment=True)

    except subprocess.CalledProcessError as e:
        # This catches Marp execution errors (e.g. syntax errors in slides)
        print(f"Marp Error: {e.stderr}")
        return {"error": "Marp failed to generate PDF", "details": e.stderr}, 500

    except Exception as e:
        # This catches Python crashes (e.g. Command not found, Permission denied)
        error_trace = traceback.format_exc()
        print(f"Server Error: {error_trace}")
        return {"error": "Internal Server Error", "details": str(e), "trace": error_trace}, 500

    finally:
        # Cleanup
        if input_filename and os.path.exists(input_filename):
            os.remove(input_filename)
        # Note: We don't delete the PDF immediately or send_file will fail. 
        # For a simple test, we leave it.

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)