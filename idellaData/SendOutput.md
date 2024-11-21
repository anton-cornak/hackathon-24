# SendOutput
[🖍 Diagram][diagram]

A global reusable sub-process used to generate, archive and deliver output in a POF-orchestrated process using the Output Management and Document microservices. When using the Global Reusable Process, an annotation symbol should be used to include the sub process parameters.

Using also the `LogInformation` GRP to log the change.
`VipsPensionsApiRequest` GRP is used to call VIPS APIs.
`StoreData` GRP is used to store process data.
`Configuration` is used to access environment variables.
`ILogger` is used to log messages, warnings, errors for developers into console. 

##  Usage
The process can be obtained using dependency injection as a service.

Use `Run` or `RunAsync` to send output:
```csharp
var sendOutputParams = new SendOutputParamsDto
{
    CorrelationId = processData.CorrelationId!, 
    CollectOutputDataSchemaName = FunctionConstants.WelcomeLetterSchemaName,
    CollectOutputDataId = processData.ProcessVariables["dossier_id"],
    TemplateName = FunctionConstants.WelcomeLetterTemplate,
    TemplateSpecificMetadata = new Dictionary<string, string>()
    {
        { "reinstatement", processData.ProcessVariables["reinstatement"] }
    },
    ArchivalInstructions = new ArchivalInstructionsDto
    {
        ArchivalRelatedEntityType = "PERSON",
        ArchivalRelatedEntityId = processData.ProcessVariables["person_id"],
        Title = "Welcomestbrief",
        SendNotification = false
    },
    DeliveryInstructions = new DeliveryInstructionsDto
    {
        DeliveryRelatedEntityType = "PERSON",
        DeliveryRelatedEntityId = processData.ProcessVariables["person_id"],
        DeliveryMethod = "MANUAL_TASK"
    }
};

await sendOutput.RunAsync(sendOutputParams, processData)
```

##  Future usage
In `Orchestrator.cs`, add to `RunAsync()` before `.CallWelcomeLetterAsync`: 
```cs
    processData = await SendOutput(processData, context);
```

Add a new private method:
```csharp
  private async Task<ProcessData> SendOutput(ProcessData processData, TaskOrchestrationContext context)
    {
        var createOutputGenerationRequestInput = new CreateOutputGenerationRequestActivityInputData
        {
            CorrelationId = processData.CorrelationId!,
            CollectOutputDataSchemaName = FunctionConstants.WelcomeLetterSchemaName,
            CollectOutputDataId = processData.ProcessVariables["dossier_id"],
            TemplateName = FunctionConstants.WelcomeLetterTemplate,
            TemplateSpecificMetadata = new Dictionary<string, string>()
        {
            { "reinstatement", processData.ProcessVariables["reinstatement"]}"}
        },
            ArchivalInstructions = new ArchivalInstructionsDto
            {
                ArchivalRelatedEntityType = "PERSON",
                ArchivalRelatedEntityId = processData.ProcessVariables["person_id"],
                Title = "Welcomestbrief",
                SendNotification = false
            },
            DeliveryInstructions = new DeliveryInstructionsDto
            {
                DeliveryRelatedEntityType = "PERSON",
                DeliveryRelatedEntityId = processData.ProcessVariables["person_id"],
                DeliveryMethod = "MANUAL_TASK"
            },
            ProcessData = processData
        };

        //createOutputGeneration: this will fail process if there is an error
        var createOutputGenerationResult = await context.CallCreateOutputGenerationRequestAsync(createOutputGenerationRequestInput);

        var checkOutputGenerationInput = new CreateOutputGenerationRequestActivityOutputData
        {
            AddOutputGenerationRequestId = createOutputGenerationResult.AddOutputGenerationRequestId,
            ProcessData = createOutputGenerationResult.ProcessData
        };

        while (true)
        {
            try
            {
                //checkOutputGeneration: this will fail process if OutputGenerationStatus = Failed or there is an error        
                var checkOutputGenerationResult = await context.CallCheckOutputGenerationStatusAsync(checkOutputGenerationInput);

                //finalizeSendOutput or SuspendProcess
                if (checkOutputGenerationResult.OutputGenerationStatus == OutputGenerationStatus.Failed)
                {
                    throw new OutputGenerationFailedException();
                }
                else if (checkOutputGenerationResult.OutputGenerationStatus == OutputGenerationStatus.Completed)
                {
                    var finalizeSendOutputInput = new CreateOutputGenerationRequestActivityOutputData
                    {
                        AddOutputGenerationRequestId = createOutputGenerationResult.AddOutputGenerationRequestId,
                        ProcessData = checkOutputGenerationResult.ProcessData
                    };

                    processData = await context.CallFinalizeSendOutputAsync(finalizeSendOutputInput);

                    break; //break loop
                }
                else if (checkOutputGenerationResult.OutputGenerationStatus == OutputGenerationStatus.Processing ||
                            checkOutputGenerationResult.OutputGenerationStatus == OutputGenerationStatus.Pending)
                {
                    //from SuspendProcess.md documentation -> Usage (might change)
                    await SuspendProcess(processData, context, createOutputGenerationResult);
                }
            }
            catch (OutputGenerationFailedException)
            {
                throw;
            }
            catch (Exception ex)
            {
                throw new SendOutputFailedException(ex);
            }
        }

        return processData;
    }
```
  
  ## This is the part of the suspend process implemented in the SendOutput method

```csharp
    private static async Task<ProcessData> SuspendProcess(ProcessData processData, TaskOrchestrationContext context, CreateOutputGenerationRequestActivityOutputData createOutputGenerationResult)
    {
        using CancellationTokenSource eventCts = new();
        using CancellationTokenSource pollingCts = new();
        using CancellationTokenSource timeoutCts = new();

        var pollingInterval = TimeSpan.FromMinutes(30);
        var maximumWaitTime = TimeSpan.FromHours(24);
        var suspendProcessInput = new SuspendProcessInput
        {
            ProcessSuspensionId = createOutputGenerationResult.AddOutputGenerationRequestId,
            MaximumWaitTime = maximumWaitTime,
            CloudEvents =
            [
                new() {
                    CloudEventType = CloudEventConstants.OutputGeneration.EventTypes.Completed,
                    Subject = createOutputGenerationResult.AddOutputGenerationRequestId
                      },
                new() {
                     CloudEventType = CloudEventConstants.OutputGeneration.EventTypes.Failed,
                     Subject = createOutputGenerationResult.AddOutputGenerationRequestId
                      }
            ],
            ProcessData = processData
        };

        processData = await context.CallSuspendedProcessAsync(suspendProcessInput);

        DateTimeOffset processSuspensionStartedAt = DateTimeOffset.UtcNow;
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
    }
```

## Exceptions
 - `SendOutputDeserializeException` - If deserializing into objects fails.
 - `OutputGenerationFailedException` - If the output generation fails.

 <!-- Links -->
[diagram]: https://confluence.visma.com/display/VII/Global+Reusable+Sub-Processes+for+Execution+Models#GlobalReusableSubProcessesforExecutionModels-SendOutput
