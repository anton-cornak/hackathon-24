# EventGridPublisher

The `EventGridPublisher` provides functionalities to publish events to Azure Event Grid using the `EventGridPublisherClient`.

## Overview

This class is designed to abstract the complexities involved in publishing events to Azure EventGrid. It encapsulates the creation of cloud events and handling of the publish response. It uses injected dependencies for event grid client provisioning, logging, and JSON serialization options which enhances flexibility and testability.


### PublishEvent
Publishes a generic event to Azure Event Grid. It constructs a `CloudEvent` from the provided event data and attempts to send it using the `EventGridPublisherClient`.

### CreateCloudEvent
A private method that constructs a `CloudEvent` instance using the provided `CloudEventData<T>`.

## Error Handling

If the event fails to publish, an error log is generated with the event type, id, status code, and reason phrase to facilitate troubleshooting.


## Configuration

This class relies on JSON serialization options provided through `IOptions<JsonSerializerOptions>`, allowing customization of how event data is serialized into JSON format.
