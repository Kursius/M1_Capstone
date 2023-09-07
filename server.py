import asyncio
import websockets
import ssl

connected_clients = set()

async def on_connect(websocket, path):
    connected_clients.add(websocket)
    
    try:
        async for message in websocket:
            if message.lower() == 'exit':
                print("Client requested to disconnect")
                break
            print(f"Received message from client: {message}")
            response = f"Server received: {message}"
            await websocket.send(response)
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        connected_clients.remove(websocket)
        print("Client disconnected.")

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain('server.crt', 'server.key')

start_server = websockets.serve(
    on_connect,
    "localhost",  # Use localhost for the server
    8765,          # Choose the port you want to use for WSS
    ssl=ssl_context
)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
