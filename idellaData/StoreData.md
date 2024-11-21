# StoreData
[🖍 Diagram](diagram)

A global reusable sub-process that updates process variables and saves their state into Azure Blob Storage.

Process variables on the `ProcessData` object should **not** be manipulated manually, instead all updates should take place through this GRP.
A process variable can only have a string value as of right now. You can store arrays and other complex structures by serializing them into a JSON string.

The state can be queried by requesting the `/processes/{process_id}` endpoint of the POF API.

##  Usage
The process can be obtained using dependency injection as a service.

Use `Run` or `RunAsync` and provide a dictionary of key-value pairs.

If a key already exists in process variables, it's updated with the provided value.
If a key is new, a new process variable is created.

```csharp
/**
* processData.ProcessVariables contains:
* {
*	{"variable_1", "apple"}
*   {"variable_2", "pear"}
* }
*/

var newVariables = new Dictionary<string, string>
            {
                { "variable_2", "banana" },
                { "variable_3", "milk" }
            };

await storeData.RunAsync(newVariables, processData);

/**
* processData.ProcessVariables contains:
* {
*	{"variable_1", "apple"}
*   {"variable_2", "banana"}
*   {"variable_3", "milk"}
* }
*
* ..and this is reflected in blob storage as well
*/
```

This is how the variables would show up when requested via POF API:
```json
{
    "process_id": "internal_tenant_a_1320fe7b-1b41-4656-a0bc-3b9a78299572",
    "tenant_id": "internal_tenant_a",
    "process_status": "FAILED",
    "process_type": "NEW_EMPLOYMENT_PARTICIPANT_1.1",
    "process_phase": "ENSURE_DOSSIER_EXISTS",
    "process_variables": {
        "variable_1": "apple",
        "variable_2": "banana",
        "variable_3": "milk"
    },
    "process_initiation_data": {},
    "process_started_at": "2024-06-28T07:14:53",
    "process_lead_time": 0,
    "correlation_Id": "9c1509c4-e51d-4579-a5a7-c7ad80d0dbe5"
}
```

As mentioned above, complex structures, like arrays, can be serialized into JSON to be stored in process variables (as process variables may only contain string values).
This is an example of what a serialized array might look like when looking at the process state through the POF API:
```json
"process_variables": {
    "scheme_ids": "[\"scheme_1\", \"scheme_2\"]"
},
```

## Exceptions
`SavingErrorException` - Exception thrown when updating the blob fails.

<!-- Links -->
[diagram]: https://confluence.visma.com/pages/viewpage.action?spaceKey=VII&title=Global+Reusable+Sub-Processes+for+Execution+Models#GlobalReusableSubProcessesforExecutionModels-StoreData