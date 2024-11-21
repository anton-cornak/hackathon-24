# HttpStartValidator

The `HttpStartValidator` class is responsible for validating HTTP request data.
It checks if headers that are required by the service are present and if the incoming body payload
contains valid `process_initiation_data`.

This service should be called from `HttpStart`, before `IStartProcess` or starting the orchestrator.

If a validation error occurs, the validator returns a `ValidationException` that is parsed by the `ExceptionHandlingMiddleware` into a 400 response with detailed description of exactly what went wrong.

## Usage
Call `ValidateAsync` from `HttpStart` to validate the incoming `HttpRequestData`. No exception handling is needed as long as the `ExceptionHandlingMiddleware` is present:
```csharp
await httpStartValidator.ValidateAsync(req);
```

Here's an example of a 400 response if a header is missing:

```json
{
    "validation_messages": [
        {
            "error_code": "POF_MISSING_REQUIRED_HEADER",
            "field": "requesting_user_id",
            "message": "Missing required header"
        }
    ],
    "status": 400,
    "error_code": "POF_INVALID_MODEL_RECIEVED_BAD_REQUEST",
    "message": "Validation Errors",
    "developer_message": "The request could not be processed because there are validation errors while processing."
}
```

Here's an example of a 400 response if the `process_initiation_data` can not be cast into a model:
```json
{
    "validation_messages": [
        {
            "error_code": "POF_INVALID_MODEL_RECIEVED_BAD_REQUEST",
            "message": "Unable to parse initiation data to type PersonBasedInitiationData."
        }
    ],
    "status": 400,
    "error_code": "POF_INVALID_MODEL_RECIEVED_BAD_REQUEST",
    "message": "Validation Errors",
    "developer_message": "The request could not be processed because there are validation errors while processing."
}
```

Here's an example of a 400 response where a field of `process_initiation_data` doesn't pass validation:
```json
{
    "validation_messages": [
        {
            "error_code": "POF_INVALID_MODEL_RECIEVED_BAD_REQUEST",
            "message": "'Initals' must be 2 characters in length. You entered 6 characters."
        }
    ],
    "status": 400,
    "error_code": "POF_INVALID_MODEL_RECIEVED_BAD_REQUEST",
    "message": "Validation Errors",
    "developer_message": "The request could not be processed because there are validation errors while processing."
}
```