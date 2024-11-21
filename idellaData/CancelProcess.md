# CancelProcess

A global reusable sub-process that cancels ( or terminates ) running process.
Along with it it sets the process status to `CANCELLED` and saves it to the blob storage.

This is also the place where the `ProcessData` object is updated.

**This is the GRP to be called from `HttpCancel` and not from an activity within the orchestrator.**
It should be called after validations have taken plae and before the Orchestrator is terminated.

##  Usage
The process can be obtained using dependency injection as a service.

Use `Run` or `RunAsync`:
```csharp
cancelProcess.RunAsync("cancelingClient", "tenantId", "instanceId", "correlationId");
```

## Exceptions
  - `UnableToCancelProcessException` - An exception is thrown when there is a problem during interacting with table or blob storage.
