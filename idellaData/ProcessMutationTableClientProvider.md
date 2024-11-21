# ProcessMutationTableClientProvider

Provides functionalities for managing pending output instances in Azure Table Storage.

## Constructor
Initializes the provider with logging and configuration to access Azure Table Storage. Throws `TableConnectionStringEmptyException` if the connection string is missing or empty.

## Usage
The following methods are present:
- `GetPendingOutputInstance`: Retrieves a pending output instance using the output generation request ID. May log `RequestFailedException` on failure.
- `AddPendingOutputInstance`: Creates a new pending output instance in the storage.
- `RemovePendingOutputInstance`: Deletes an existing pending output instance from the storage.

## Exceptions
- `TableConnectionStringEmptyException`: Thrown during initialization if the connection string is not provided.
- `RequestFailedException`: Logged on failures to interact with Azure Table Storage. Does not halt execution.