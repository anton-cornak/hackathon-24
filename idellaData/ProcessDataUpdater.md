# ProcessDataUpdater

The `ProcessDataUpdater` provides low-level functionality to save process data to Azure Blob Storage.
It's sometimes used by higher level GRPs to update the process state, but can be used manually.

When connected to local storage (`UseDevelopmentStorage=true`), index tags don't work at all due to an [Azurite limitation](azurite-limitation).
In fact, they will crash the program, thus it's not even attempted to insert them.

## Usage
Call `Save` or `SaveAsync`:

```csharp
await processDataUpdater.SaveAsync(processData);
```

## Exceptions
- `ProcessVariablesConnectionStringIsEmptyException`: Blob store connection string is null or empty
- `TenantIdIsNullException`: Tenant ID on ProcessData is null or empty
- `ProcessDataDeserializeException`: Error deserializing process state when attempting to update it

<!-- Links -->
[azurite-limitation]: https://github.com/Azure/Azurite/issues/647
