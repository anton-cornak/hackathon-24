# FailProcess
[🖍 Diagram](diagram)

A global reusable sub-process that completes a process by setting the status to `FAILED` and the outcome to a specified string value.
It also raises the `process.v1.failed` event.

##  Usage
The process can be obtained using dependency injection as a service.

Use `Run` or `RunAsync` to fail a process.
```csharp
await failProcess.RunAsync("Something messed up!", processData.ProcessPhase, processData.ProcessOutcome, processData);
```

 <!-- Links -->
 [diagram]: https://confluence.visma.com/pages/viewpage.action?spaceKey=VII&title=Global+Reusable+Sub-Processes+for+Execution+Models#GlobalReusableSubProcessesforExecutionModels-FailProcess