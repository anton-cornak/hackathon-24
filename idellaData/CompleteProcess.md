# CompleteProcess
[🖍 Diagram](diagram)

A global reusable sub-process that completes a process by setting the status to `COMPLETED` and the outcome to a specified string value.
Usually called at the end of a process workflow.

##  Usage
The process can be obtained using dependency injection as a service.

Use `Run` or `RunAsync`: to complete a process.
```csharp
await completeProcess.RunAsync(string outcome, ProcessData processData)
```

 <!-- Links -->
 [diagram]: https://confluence.visma.com/pages/viewpage.action?spaceKey=VII&title=Global+Reusable+Sub-Processes+for+Execution+Models#GlobalReusableSubProcessesforExecutionModels-CompleteProcess