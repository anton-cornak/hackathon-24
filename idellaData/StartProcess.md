# StartProcess
[🖍 Diagram](diagram)

A global reusable sub-process that starts new process.
Along with it it sets the process status to `RUNNING`, sets the process initiation data and saves it to the blob storage.

This is also the place where the `ProcessData` object is created.

**This is the only GRP to be called from `HttpStart` and not from an activity within the orchestrator.**
It should be called after validations have taken plae and before the Orchestrator is started.

##  Usage
The process can be obtained using dependency injection as a service.

Use `Run` or `RunAsync`:
```csharp
startProcess.RunAsync("startingClient", "tenantId", processInitiationData, "correlationId");
```

<!-- Links -->
[diagram]: https://confluence.visma.com/pages/viewpage.action?spaceKey=VII&title=Global+Reusable+Sub-Processes+for+Execution+Models#GlobalReusableSubProcessesforExecutionModels-(re)start_process
