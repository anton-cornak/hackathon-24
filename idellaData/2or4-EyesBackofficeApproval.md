# 2or4-EyesBackofficeApproval
[🖍 Diagram](diagram)

A global reusable sub-process that can be used to insert an approval from the one or two backoffice users, also known as a 2-eyes or 4-eyes check. 
The process will be suspended until the task is completed, with either an APPROVED or DENIED outcome.

## Usage
The process can be obtained using dependency injection as a service.

Use `Run` or `RunAsync` to create approval tasks.
```cs
backofficeApproval.RunAsync(backofficeData, processData)
```

Here is an example of a log record:
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

##  Future usage
In `Orchestrator.cs`, add to `RunAsync()`:
```cs
    private static async Task<Tuple<ProcessData, bool>> BackofficeApproval(TaskOrchestrationContext context, ProcessData processData)
    {
        ///<summary>
        ///This variable should contain the data that will be sent to the backoffice approval service.
        ///Link for the diagram: https://lucid.app/lucidchart/8f3d64fa-bbee-4cfa-9cfa-9c6c3498ba2e/edit?callback=https%3A%2F%2Fconfluence.visma.com%2Fplugins%2Flucidchart%2FupdateDiagram.action%3FcontentId%3D639390268%26attachment%3D2%2Bor%2B4-eyes%2Bbackoffice%2Bapproval%2BGlobally%2BReusable%2BSubprocess%26lcId%3D8bd55f5b-38aa-4453-a5be-b4a51f9a7240%26documentToken%3Dv2_49e3fa53c4ee03fb4c0ffc36f7b098351aa454da31416c7049aaadd54cd19970-a%253D103224718%2526c%253Db6ccec46f1fc3168e7db48a97177d1ea63509e36%2526d%253D8f3d64fa-bbee-4cfa-9cfa-9c6c3498ba2e%2526p%253D&name=confluenceserver&useCachedRole=false&oauth_nonce=1681544307&oauth_signature=2F%2FRZtcq7lC0YZzJfIKMetwIpD4%3D&oauth_token=179ea0979fd59a4a48240be558325e6864b97668&oauth_consumer_key=b6ccec46f1fc3168e7db48a97177d1ea63509e36&oauth_timestamp=1721025546&oauth_signature_method=HMAC-SHA1&oauth_version=1.0&page=0_0#
        ///</summary
        var backoffice = new BackofficeApprovalInputData
        {
            ProcessId = processData.ProcessId,
            Origin = processData.ProcessType,
            TaskCode = "taskCode",
            Title = "title",
            Description = "description",
            RequestingUserId = "requestingUserId",
            RequestingUserRole = RequestingUserRole.BackofficeUser,
            PollingInterval = TimeSpan.FromHours(4),
            MaximumWaitTime = TimeSpan.FromDays(14),
            Priority = 50,
            ReferenceId = Guid.NewGuid().ToString(),
            CorrelationId = Guid.NewGuid().ToString(),
            CausationId = Guid.NewGuid().ToString(),
            RelatedEntity = "relatedEntityId",
            BucketId = "bucketid",
            BucketName = "bucketName",
            StartDateTime = DateTime.UtcNow,
            DueDateTime = DateTime.UtcNow,// *DueDateTime is exclusive with DueDateOffset*
            //DueDateOffset = new DueDateOffsetDto
            //{
            //    NumberOfDays = 0,
            //    OffsetType = DateOffsetType.BusinessDays
            //}
        };

        try
        {
            var tuple = (ProcessData: processData, Backoffice: backoffice);

            processData = await context.CallCreateApprovalTaskAsync(Tuple.Create(tuple.ProcessData, tuple.Backoffice));
            var percentComplete = 0;
            var chosenOutcome = string.Empty;

            while (true)
            {
                var approvalTupple = await context.CallCheckApprovalCompleteAndOutcomeAsync(processData);
                processData = approvalTupple.Item1;
                var task = approvalTupple.Item2;

                object? percentCompleteValue = task[ProcessDataConstants.PercentComplete];
                object? chosenOutcomeValue = task[ProcessDataConstants.ChosenOutcome];

                // Check if 'chosenOutcomeValue' exists and is not null before calling ToString()
                if (chosenOutcomeValue is not null)
                {
                    chosenOutcome = chosenOutcomeValue.ToString();
                }
                // Safely cast 'percentCompleteValue' to int if it's not null; otherwise, keep it as 0.
                percentComplete = percentCompleteValue != null ? Convert.ToInt32(percentCompleteValue) : 0;

                if (percentComplete.Equals(100) && !string.IsNullOrWhiteSpace(chosenOutcome))
                {
                    break;
                }
                else
                {
                    var processSuspensionId = processData.ProcessVariables[$"{backoffice.TaskCode}_task_id"];

                    if (string.IsNullOrWhiteSpace(processSuspensionId))
                    {
                        throw new ArgumentException("TaskId cannot be null when suspending the process");
                    }

                    processData = await SuspendProcess(context, processData, backoffice, processSuspensionId);
                }
            }

            processData = await context.CallFinalizeTaskOutcomeAsync(Tuple.Create(processData, backoffice, chosenOutcome));

            if (chosenOutcome.Equals("APPROVED"))
            {
                return Tuple.Create(processData, true);
            }
            else if (chosenOutcome.Equals("DENIED"))
            {
                return Tuple.Create(processData, false);
            }
        }
        catch (TaskFailedException ex) when (ex.FailureDetails.IsCausedBy<BaseBackofficeApprovalException>())
        {
            throw new CreateOrCheckApprovalTaskInOrchestratorException(ex);
        }

        return Tuple.Create(processData, false);
    }
```
  
  ## This is the part of the suspend process implemented in the SendOutput method

```csharp
    private static async Task<ProcessData> SuspendProcess(TaskOrchestrationContext context, ProcessData processData, BackofficeApprovalInputData backoffice, string processSuspensionId)
    {
        using CancellationTokenSource eventCts = new();
        using CancellationTokenSource pollingCts = new();
        using CancellationTokenSource timeoutCts = new();

        var suspendProcessInput = new SuspendProcessInput
        {
            ProcessSuspensionId = processSuspensionId!,
            MaximumWaitTime = backoffice.MaximumWaitTime,
            CloudEvents =
              [
                  new()
                  {
                      CloudEventType=CloudEventConstants.TaskManagement.EventTypes.Completed,
                      Subject=processSuspensionId
                  },
                  new()
                  {
                      CloudEventType=CloudEventConstants.TaskManagement.EventTypes.Cancelled,
                      Subject=processSuspensionId
                  },
                  new()
                  {
                      CloudEventType=CloudEventConstants.TaskManagement.EventTypes.Deleted,
                      Subject=processSuspensionId
                  }
              ],
            ProcessData = processData
        };

        processData = await context.CallSuspendedProcessAsync(suspendProcessInput);

        DateTimeOffset processSuspensionStartedAt = DateTimeOffset.UtcNow;

        Task eventTask = WaitForExternalEvent(context, eventCts.Token);
        Task pollingTask = WaitForNextPolling(context, processSuspensionStartedAt, backoffice.PollingInterval, pollingCts.Token);
        Task timeoutTask = WaitForTimeout(context, processSuspensionStartedAt, backoffice.MaximumWaitTime, timeoutCts.Token);

        Task firstTaskToFinish = await Task.WhenAny(eventTask, pollingTask, timeoutTask);

        if (firstTaskToFinish == eventTask)
        {
            pollingCts.Cancel();
            timeoutCts.Cancel();

            return processData;
        }

        if (firstTaskToFinish == pollingTask)
        {
            eventCts.Cancel();
            timeoutCts.Cancel();

            return processData;
        }

        eventCts.Cancel();
        pollingCts.Cancel();

        throw new TimeExpiredException(backoffice.MaximumWaitTime);
    }
```

## Exceptions
- `CreateOrCheckApprovalTaskInOrchestratorException` - Thrown when an error occurs during the creation or checking of the approval task in orchestrator.`
- `CreateApprovalException`- Thrown when an error occurs during the creation of the 2-4 eyes approval task.`
- `CheckApprovalException` - Thrown when an error occurs during the checking of the 2-4 eyes approval task. Task can be deleted or cancelled.`
- `TaskIsCancelledException` - Thrown when the task is cancelled when checking for approval.
- `TaskIsDeletedException` - Thrown when the task is deleted when checking for approval.

<!-- Links -->
[diagram]: https://confluence.visma.com/display/VII/Global+Reusable+Sub-Processes+for+Execution+Models#GlobalReusableSubProcessesforExecutionModels-SendOutput
