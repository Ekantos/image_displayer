import os
import json
import asyncio
import websockets
import threading
import http.server
import socketserver

# Function to get the last modified image name in the folder
async def get_last_image_name():
    image_folder_path = "images"  # Assume the image folder is in the same directory as web_server.py
    image_names = [f for f in os.listdir(image_folder_path) if os.path.isfile(os.path.join(image_folder_path, f))]
    if not image_names:
        return None

    latest_image = max(image_names, key=lambda f: os.path.getmtime(os.path.join(image_folder_path, f)))
    return latest_image

# WebSocket server function to publish the last modified image name
async def image_publisher(websocket, path):
    current_image = None

    while True:
        latest_image = await get_last_image_name()
        if latest_image != current_image:
            current_image = latest_image
            if current_image:
                await websocket.send(json.dumps(current_image))

        await asyncio.sleep(2)  # Check for updates every 2 seconds

# Web server function to serve the HTML page and JavaScript for the client
def start_web_server():
    PORT = 8000
    Handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("Serving at port", PORT)
        httpd.serve_forever()

# Run the WebSocket server in its own event loop
async def run_ws_server():
    ws_server = await websockets.serve(image_publisher, "localhost", 8000)
    await ws_server.wait_closed()

# Start the web server on a separate thread
web_server_thread = threading.Thread(target=start_web_server)
web_server_thread.start()

# Run the WebSocket server in the main thread
asyncio.get_event_loop().run_until_complete(run_ws_server())
