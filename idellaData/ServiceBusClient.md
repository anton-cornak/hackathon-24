# ServiceBusClient

The `ServiceBusClient` class enabling interaction with Azure Service Bus for the specific purpose of retrieving output generation events based on request ID.

## Usage

- `GetSendOutputOutputgenerationEventsForRequestId`: Subscribes to a Service Bus topic and waits for a specific event related to a request ID. It then processes these events asynchronously.
