# SendOutputTableClientProvider

**This is a helper service for `SendOutput`. There is probably no reason to use this manually on your own.**

Provides low-level Azure Table Storage management for pending output instances.

## Usage

- `GetPendingOutputInstance`: Retrieves a specific pending output instance by ID and returns null if no instance is found.
- `AddPendingOutputInstance`: Adds a new pending output instance and uses current UTC time for the start datetime.
- `RemovePendingOutputInstance`: Removes a specified pending output instance by ID.

## Exceptions
- **TableConnectionStringEmptyException:** Thrown if initialization receives an empty Azure Table connection string.
- **RequestFailedException:** Logged within method operations when Azure Table actions fail.