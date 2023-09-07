import asyncio
import websockets
import ssl

async def hello():
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)

    # Load the trusted CA certificate for verification
    ssl_context.load_verify_locations('server.crt')

    async with websockets.connect(
        "wss://localhost:8765",  # Connect to localhost on the same port
        ssl=ssl_context
    ) as websocket:
        try:
            while True:
                message = input("Enter a message (or 'exit' to quit): ")
                if message.lower() == 'exit':
                    break  # Exit the loop and close the connection
                await websocket.send(message)
                response = await websocket.recv()
                print(f"Server says: {response}")
        except websockets.exceptions.ConnectionClosed:
            print("Client disconnected")

asyncio.get_event_loop().run_until_complete(hello())
