# VipsPensionsApiRequest
[🖍 Diagram](diagram)

A global reusable sub-process responsible for sending requests to the VIPS Pensions API, including getting an access token, constructing requests, and handling responses. It also includes robust error handling.

## Usage
The process can be obtained using dependency injection as a service.

Use `SendRequest` or `SendRequestAsync`:

```csharp
var response = await vipsPensionsApiRequest.SendRequestAsync(
    ApiMethod.GET, 
    "dossier-creation-mutations/{mutation_id}", 
    processData, 
    parameters: new Dictionary<string, string> { {"queryParam", "value"} },
    pathParameters: new Dictionary<string, string> {{"mutation_id", "12345"}},
    headers: new Dictionary<string, string> {{"Custom-Header", "value"}},
    requestBody: null
);
```

This snippet demonstrates sending a `GET` request to the VIPS Pensions API (namely the `dossier-creation-mutations/{mutation_id}` endpoint) and returns the API's response as a string.

## Idempotency Key
For `POST` and `PATCH` methods, an idempotency key is added to the request headers to prevent duplicate submissions during retries. This key is automatically generated and unique for each request.
This ensures that if the same request is accidentally sent multiple times, the server will recognize it and prevent duplicate processing of the request.

Adding an `idempotency_key` header manually won't cause any errors, the manually added key will be preferred instead of generating a random one.

## Example console logs
Each request sent logs the request in detail using the standard logger:
```plaintext
VIPS Pensions API token received and parsed
Method: GET
URL: https://apim-vips-dev-shared-vid.azure-api.net/pensions/contracts?employer=string&cost_center_name=string
Query params: {"employer":"string","cost_center_name":"string"}
Body:
Sending HTTP request GET https://apim-vips-dev-shared-vid.azure-api.net/pensions/contracts?employer=string&cost_center_name=string
Received HTTP response headers after 481.9844ms - 200
End processing HTTP request after 483.8929ms - 200
VIPS Pensions API Request successful. Response: {"pagination":{"total":0,"offset":0,"limit":20},"items":[]}
Pension API response: {"pagination":{"total":0,"offset":0,"limit":20},"items":[]}
```


## Exceptions
 Exceptions the VipsPensionsApiRequest might throw:

- `TenantIdNotFoundException` - Occurs when the tenant ID is missing on the provided ProcessData.
- `VipsPensionsApiRequestParseTokenException` - Triggered during failure to parse the API access token.
- `InvalidApiMethodException` - Thrown when an unsupported API method is used.
- `NotFoundException` - Indicates a 404 response from the API.
- `UnexpectedErrorException` - Catches all other errors that don't fall into the above categories.

 <!-- Links -->
 [diagram]: https://confluence.visma.com/pages/viewpage.action?spaceKey=VII&title=Global+Reusable+Sub-Processes+for+Execution+Models#GlobalReusableSubProcessesforExecutionModels-ChangePhaseOrOutcome