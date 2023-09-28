import asyncio
from bless import (
    BlessServer,
    GATTCharacteristicProperties,
    GATTAttributePermissions
)

#Randomly generated UUIDs, feel free to replace with your own UUIDs
service_uuid = "d63c692b-fe49-4031-aa78-5b39cec3e7eb"
message_uuid = "789a3815-cdde-4e65-aa97-bdf0802b856d"

messageCount = 0

#Send the stored message back to the client
def read_request(characteristic):
    response = characteristic.value
    print("Send:", response.decode("utf-8"))
    return response

#Get the message from the client, add a message count prefix to it, and store it
def write_request(characteristic, value):
    global messageCount
    messageCount += 1
    message = value.decode('utf-8')
    print("Receive:", message)
    store_value = f"[Message #{messageCount}] {message}"
    store_value = bytearray(store_value, "utf-8")
    characteristic.value = store_value

#Setup the server
async def main():
    server = BlessServer(name="Test Server")
    await server.add_new_service(service_uuid)

    char_flags = (
            GATTCharacteristicProperties.read |
            GATTCharacteristicProperties.write
            )
    permissions = (
            GATTAttributePermissions.readable |
            GATTAttributePermissions.writeable
            )
    await server.add_new_characteristic(
        service_uuid,
        message_uuid,
        char_flags,
        None,
        permissions
    )

    server.read_request_func = read_request
    server.write_request_func = write_request

    await server.start()
    print("Server started. Waiting for messages...")
    try:
        #Keep the server running forever
        while True:
            await asyncio.sleep(60*60)
    #Allows the server to stop gracefully for keyboard interrupts
    except:
        print("Shutting down server...")
        await server.stop()

asyncio.run(main())