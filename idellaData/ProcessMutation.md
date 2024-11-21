# Process Mutation

:chart_with_upwards_trend: [Global Reusable Sub-Processes for Execution Models](https://confluence.visma.com/pages/viewpage.action?spaceKey=VII&title=Global+Reusable+Sub-Processes+for+Execution+Models)


This code snippet outlines the process of creating a dossier by submitting a mutation, checking its status, and handling the mutation state.

## Mutation Creation
1. A `ProcessMutationInput` object is initialized with properties for the mutation, including definition name, process data, and specific properties related to the dossier creation.
2. This mutation input is then submitted asynchronously using `CallCreateMutationAsync` method.

## Status Checking Loop
1. Enters a loop to continuously check the status of the mutation until it is either completed, rejected, or an error occurs.
2. Utilizes `CallCheckMutationStatusAsync` method to query the current state of the mutation.
3. Extracts the mutation ID from process variables and checks if the status for this mutation ID exists.
4. Based on the mutation status (`ACTIVE`, `ERROR`, `REJECTED`), appropriate actions are taken:
   - **ACTIVE**: Calls `CallProcessCompletedMutationAsync` to process the mutation as completed.
   - **ERROR** or **REJECTED**: Calls `CallProcessFailedMutationAsync` to handle the failure.
   - Any other state leads to suspending the mutation processing with a call to `CallSuspendedProcessAsync`, implementing a wait time and polling interval.

##  Input - DossierCreationMutation
Following block of code to be used in the `Orchestrator` function to Dossier creation mutation:
```csharp
var input = new ProcessMutationInput
{
    MutationDefinitionName = "migration_dossier",
    ProcessData = processData,
    MutationType = MutationType.DOSSIER_CREATION,
    MutationProperties = new Dictionary<string, object>
    {
        { "birth_date", "1990-04-09" },
        { "sex", "MALE"},
        { "surname", "Martin" },
    }
};
```

##  Input - DossierMutation
Following block of code to be used in the `Orchestrator` function to Dossier mutation:
```csharp
processData.ProcessVariables.Add("dossier_id", "0000009876");

var input = new ProcessMutationInput
{
    MutationDefinitionName = "add_policy",
    ProcessData = processData,
    MutationType = MutationType.DOSSIER,
    PathParam = "0000009876", // dossier_id
    MutationProperties = new Dictionary<string, object>
    {
        { "employer_id", "164" },
        { "scheme_id", "9917"},
        { "employment_start_date", "2024-01-01" },
    }
};
```


##  Input - PolicyMutation
Following block of code to be used in the `Orchestrator` function to Policy mutation:
```csharp
processData.ProcessVariables.Add("policy_id", "0000009872-1");

var input = new ProcessMutationInput
{
    MutationDefinitionName = "add_income",
    ProcessData = processData,
    MutationType = MutationType.POLICY,
    PathParam = "0000009872-1", // policy_id
    MutationProperties = new Dictionary<string, object>
    {
        { "amount", 1 },
        { "period_number", 1 },
        { "payment_date", "2022-01-01" },
        { "period_year", 2022 }
    }
};
```

##  Usage
Following block of code to be used in the `Orchestrator` function to Dossier creation mutation:
```csharp
ProcessMutationInput processMutationInput = await CreateMutation(context, processData);
processData = processMutationInput.ProcessData!;

await context.CreateTimer(TimeSpan.FromSeconds(30), CancellationToken.None);

string mutationIdKey = $"mutation_id_for_{processMutationInput.MutationDefinitionName}";
string mutationId = processData.ProcessVariables[mutationIdKey];

while (true)
{
    processData = await context.CallCheckMutationStatusAsync(processMutationInput);

    MutationState mutationState = GetMutationState(processData, mutationId);

    if (mutationState is MutationState.Error or MutationState.Rejected)
    {
        _ = await FailMutation(context, processData, mutationState);
        throw new MutationFailedException($"Mutation {mutationId} cannot be processed because its state is {mutationState}");
    }

    if (mutationState is MutationState.Active)
    {
        processData = await CompleteMutation(context, processData, processMutationInput.MutationType);
        break;
    }

    processData = await SuspendProcess(context, processData, mutationId);
    processMutationInput.ProcessData = processData;
}
```

The following helper methods must be defined as well in the same orchestrator or sub-orchestrator:
```csharp
private static async Task<ProcessMutationInput> CreateMutation(TaskOrchestrationContext context, ProcessData processData)
{
    ProcessMutationInput processMutationInput = new()
    {
        // ..depending on your mutation type
    };

    processData = await context.CallCreateMutationAsync(processMutationInput);
    processMutationInput.ProcessData = processData;

    return processMutationInput;
}

private static MutationState GetMutationState(ProcessData processData, string mutationId)
{
    string variableKey = $"mutation_status_for_mutation_id_{mutationId}";
    if (processData.ProcessVariables.TryGetValue(variableKey, out string? mutationStateVariable))
    {
        if (Enum.TryParse(mutationStateVariable, out MutationState mutationState))
        {
            return mutationState;
        }

        throw new ProcessMutationStateNotDefinedException();
    }

    throw new ProcessVariablesDoesNotContainMutationStateException();
}

private static async Task<ProcessData> SuspendProcess(TaskOrchestrationContext context, ProcessData processData, string processSuspensionId)
{
    TimeSpan maximumWaitTime = TimeSpan.FromHours(48);
    TimeSpan pollingInterval = TimeSpan.FromMinutes(10);

    SuspendProcessInput suspendProcessInput = new()
    {
        ProcessSuspensionId = processSuspensionId,
        ProcessData = processData,
        MaximumWaitTime = maximumWaitTime,
        CloudEvents = new List<SuspendProcessCloudEvent>
        {
            new()
            {
                CloudEventType = CloudEventConstants.PolicyAdministration.EventTypes.Created,
                Subject = processSuspensionId
            },
            new()
            {
                CloudEventType = CloudEventConstants.PolicyAdministration.EventTypes.Updated,
                Subject = processSuspensionId
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

    throw new TimeExpiredException(); // TODO: Provide timeout value when new toolkit version is released
}

private static async Task<ProcessData> FailMutation(TaskOrchestrationContext context, ProcessData processData, MutationState state)
{
    ProcessFailedMutationInput processFailedMutationInput = new()
    {
        MutationState = state,
        ProcessData = processData
    };

    processData = await context.CallProcessFailedMutationAsync(processFailedMutationInput);

    return processData;
}

private static async Task<ProcessData> CompleteMutation(TaskOrchestrationContext context, ProcessData processData, MutationType mutationType)
{
    ProcessCompletedMutationInput processCompletedMutationInput = new()
    {
        MutationType = mutationType,
        ProcessData = processData
    };

    processData = await context.CallProcessCompletedMutationAsync(processCompletedMutationInput);

    return processData;
}

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

## Exception Handling
- Throws `ProcessMutationStateNotDefinedException` if the mutation status is not retrievable.
- Throws `ProcessVariablesDoesNotContainMutationStateException` if the process variables do not contain the mutation status.

## Process Suspension
Implements a suspension logic that waits for a specific amount of time (`P2D`) with polling intervals (`PT10M`) and listens for specific cloud event types before finalizing the suspension process.

## Key Functions Used
- `CallCreateMutationAsync`: Submits a mutation request.
- `CallCheckMutationStatusAsync`: Checks the current status of a mutation.
- `CallProcessFailedMutationAsync`: Processes a failed mutation.
- `CallProcessCompletedMutationAsync`: Processes a successfully completed mutation.
- `CallSuspendedProcessAsync`: Suspends the mutation process based on specific conditions.
