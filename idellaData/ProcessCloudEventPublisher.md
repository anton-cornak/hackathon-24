# ProcessCloudEventPublisher

The `ProcessCloudEventPublisher` is tasked with publishing different types of process-related cloud events to Azure Event Grid through `IEventGridPublisher`.

## Overview

Designed to facilitate the publication of process-related events, such as process completion, failure, and startup events, this class abstracts the details of creating and sending cloud events to Azure Event Grid. It relies on a provided implementation of `IEventGridPublisher` to handle the actual event publishing.

## Methods

### PublishCompletedCloudEvent
Publishes a completed process event to Azure Event Grid.

### PublishFailedCloudEvent
Publishes a failed process event to Azure Event Grid.

### PublishUnexpectedErrorInVipsOccurredCloudEvent
Publishes an unexpected error event in a VIP (Very Important Process) to Azure Event Grid.

### PublishStartedCloudEvent
Publishes a started process event to Azure Event Grid.
