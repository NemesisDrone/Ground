# Communication Server

This script establishes a communication server for exchanging data between the server and the drone. 
It relies on Redis as a message broker to facilitate communication. 
The server listens on a specified host and port for incoming drone connections, manages message transmission, 
and it detects the drone's connection status.

All messages from the drone are published on redis, and then forwarded to redis-channel by /backend/services/messages_forwarder.py to be received on the frontend ui using websockets.
The frontend sends messages on redis, and then the server forwards them to the drone.

## Global Redis variable
- IS_DRONE_CONNECTED: boolean, true if the drone is connected, false otherwise
- LAST_HEARTBEAT_RECEIVED: timestamp, the last time a heartbeat was received from the drone
- LAST_HEARTBEAT_SENT: timestamp, the last time a heartbeat was sent to the drone