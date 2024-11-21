# LogInformation
[🖍 Diagram](diagram)

A global reusable sub-process that saves a log entry into Azure Table storage.
Not only does it save the message, but also captures the process state.
These log entries can be queried through the POF API using the `/processes/{process_id}/logs` endpoint.

Note that this GRP should not be used in place of the standard [`ILogger`](ilogger) interface provided by Microsoft and should not be relied upon to log messages into the log output files or console.

Process diagrams usually explicitly determine when this GRP should be called.

##  Usage
The process can be obtained using dependency injection as a service.

Use `Run` or `RunAsync` to log a message:
```csharp
await logInformation.RunAsync("hello world", processData);
```

Here is an example of a log record:
```json
{
    "timestamp": "2024-05-31T20:33:35.853Z",
    "process_id": "internal_tenant_a_01e04600-6c6f-412a-9835-0a8dbdd6fc6d",
    "tenant_id": "internal_tenant_a",
    "process_type": "INCOME_PERIOD_CHANGE_1.1",
    "process_status": "RUNNING",
    "text": "hello world"
}
```

## Exceptions
  - `TableConnectionStringEmptyException` - An exception is thrown when the Azure Table connection string is empty.
  - `TenantIdMissing` - An exception is thrown when ProcessData has a null or empty TenantId field.
  - `FailedToAddTableRow` - An exception is thrown when Azure Table is unable to add a log entry.
  - `TableNotProvisionedException` - An exception is thrown when a table for the provided tenant does not exist.

<!-- Links -->
[diagram]: https://confluence.visma.com/pages/viewpage.action?spaceKey=VII&title=Global+Reusable+Sub-Processes+for+Execution+Models#GlobalReusableSubProcessesforExecutionModels-LogInformation

[ilogger]: https://learn.microsoft.com/en-us/dotnet/api/microsoft.extensions.logging.ilogger?view=net-8.0