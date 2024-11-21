# SuspendProcess
[🖍 Diagram][diagram]

This SubProcess is used to have the POF-orchestrated process go into a suspended mode, where it is not incurring unnecessary costs. 
This is used where the process is waiting for something external. 
This global reusable subprocess can only be placed on the main line of the Process.
While waiting for an external event, the process will be suspended until the event is received or a timeout is reached and the timeout exception is thrown.

##  Usage
Following code is to be used in the `Orchestrator` function directly to suspend the process:
```csharp

TimeSpan maximumWaitTime = TimeSpan.FromDays(31);
TimeSpan pollingInterval = TimeSpan.FromHours(4);

// Prepare suspend process data
SuspendProcessInput suspendProcessInput = new()
{
    ProcessSuspensionId = processSuspensionId,
    ProcessData = processData,
    MaximumWaitTime = maximumWaitTime,
    CloudEvents = new List<SuspendProcessCloudEvent>
    {
        // Replace this with a list of events you want your process to wake up to
        new()
        {
            CloudEventType = CloudEventConstants.TaskManagement.EventTypes.Completed,
            Subject = "subject"
        }
    }
};

processData = await context.CallSuspendedProcessAsync(suspendProcessInput);

DateTimeOffset processSuspensionStartedAt = DateTimeOffset.Parse(processData.ProcessVariables[$"process_suspension_{processSuspensionId}_started_at"]);

using CancellationTokenSource eventCts = new();
using CancellationTokenSource pollingCts = new();
using CancellationTokenSource timeoutCts = new();

Task eventTask = WaitForExternalEvent(context, eventCts.Token);
Task pollingTask = WaitForNextPolling(context, processSuspensionStartedAt, pollingInterval, pollingCts.Token);
Task timeoutTask = WaitForTimeout(context, processSuspensionStartedAt, maximumWaitTime, timeoutCts.Token);

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

throw new TimeExpiredException(maximumWaitTime);
```

The following helper methods must be defined as well in the same orchestrator or sub-orchestrator:
```csharp
private static Task WaitForExternalEvent(TaskOrchestrationContext context, CancellationToken token)
{
    const string resumeProcessEventName = "ResumeProcess";
    return context.WaitForExternalEvent<string>(resumeProcessEventName, token);
}

private static Task WaitForNextPolling(TaskOrchestrationContext context, DateTimeOffset processSuspensionStartedAt, TimeSpan pollingInterval, CancellationToken token)
{
    DateTimeOffset nextPollingAt = processSuspensionStartedAt.Add(pollingInterval);
    while (nextPollingAt < context.CurrentUtcDateTime)
    {
        nextPollingAt = nextPollingAt.Add(pollingInterval);
    }
    return context.CreateTimer(nextPollingAt.UtcDateTime, token);
}

private static Task WaitForTimeout(TaskOrchestrationContext context, DateTimeOffset processSuspensionStartedAt, TimeSpan maximumWaitTime, CancellationToken token)
{
    TimeSpan delayToAllowPollingBeforeTimeout = TimeSpan.FromSeconds(10);
    DateTimeOffset maximumWaitTimeElapsedAt = processSuspensionStartedAt.Add(maximumWaitTime).Add(delayToAllowPollingBeforeTimeout);
    return context.CreateTimer(maximumWaitTimeElapsedAt.UtcDateTime, token);
}
```
This is only the final part of the suspend process functionality. 
It will be preceded by suspend process activity function which takes care of registering the process for resuming.
Also the `ResumeProcess` function should be implemented to resume the process.

 <!-- Links -->
[diagram]: https://confluence.visma.com/pages/viewpage.action?spaceKey=VII&title=Global+Reusable+Sub-Processes+for+Execution+Models#GlobalReusableSubProcessesforExecutionModels-SuspendProcess
