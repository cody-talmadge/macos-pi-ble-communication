import asyncio
from bleak import BleakClient, BleakScanner, BleakError

#Randomly generated UUIDs, feel free to replace with your own UUIDs
#as long as they match the server's UUIDs
service_uuid = "d63c692b-fe49-4031-aa78-5b39cec3e7eb"
message_uuid = "789a3815-cdde-4e65-aa97-bdf0802b856d"

async def main():

    #Search for the Pi's server address
    server_address = None
    print("Searching for server...")
    while not server_address:
        devices = await BleakScanner.discover(service_uuids = [service_uuid])
        if devices:
            server_address = devices[0].address
            print("Found server at: ", server_address)
            break
        print("Server not found, searching again...")

    print("Server found, connecting to server")
    #Try to connect to the server until successful
    while True:
        try:
            async with BleakClient(server_address, timeout=30) as client:
                print("Connected to server!")
                while True:
                    message = input("Send: ")
                    message = bytearray(message, "utf-8")
                    await client.write_gatt_char(message_uuid, message)
                    response = await client.read_gatt_char(message_uuid)
                    response = response.decode('utf-8')
                    print("Receive:", response)
        except BleakError as e:
            print("Error:", e)
            print("Trying to reconnect...")
            await asyncio.sleep(1)

asyncio.run(main())