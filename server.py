import http.server
import socketserver
import os
import sys

PORT = 8000

def run_server():
    try:
        # Get the project root directory (two levels up from this script)
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        # Change to the src directory
        src_dir = os.path.join(project_root, 'src')
        if not os.path.exists(src_dir):
            raise FileNotFoundError(f"Source directory not found at: {src_dir}")
        
        os.chdir(src_dir)
        print(f"Serving files from: {src_dir}")
        
        Handler = http.server.SimpleHTTPRequestHandler
        Handler.extensions_map.update({
            '.js': 'application/javascript',
            '.css': 'text/css',
        })

        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print(f"Server running at: http://localhost:{PORT}")
            print("Press Ctrl+C to stop the server")
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\nShutting down server...")
        sys.exit(0)
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_server() 