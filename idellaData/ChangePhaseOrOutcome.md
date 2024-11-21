# ChangePhaseOrOutcome
[🖍 Diagram](diagram)

A global reusable sub-process that changes the phase or outcome of a process and updating process data.

##  Usage
The process can be obtained using dependency injection as a service.

Use `Run` or `RunAsync` to change the phase or outcome:
```csharp
await changePhaseOrOutcome.RunAsync(processData,"phase", "outcome");
```
The phase and outcome are available as fields in the process status blob:
```json
   {
        "timestamp": "2024-05-28T13:31:43.516Z",
        "process_id": "internal_tenant_a_065c5c6f-eaa4-46d8-8ed8-d27cd43cbc8e",
        "tenant_id": "internal_tenant_a",
        "process_type": "NEW_EMPLOYMENT",
        "process_status": "Failed",
        "process_phase": "CHECKING_CONTRACT",
        "text": "Cannot find Contract for Employer"
    }
```

## Exceptions
 `SavingException` - An exception is thrown when the process fails to save data to Azure Table Storage.
 <!-- Links -->
 [diagram]: https://confluence.visma.com/pages/viewpage.action?spaceKey=VII&title=Global+Reusable+Sub-Processes+for+Execution+Models#GlobalReusableSubProcessesforExecutionModels-ChangePhaseOrOutcome