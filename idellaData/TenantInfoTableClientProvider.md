# TenantInfoTableClientProvider
This class is responsible for managing tenant information within the `poftenantinfo` Azure Table.

which holds Tenant IDs and their  It provides functionalities to retrieve tenant IDs based on environmental and tenant key parameters, ensuring access to tenant data is streamlined and centralized.

## Overview
The `TenantInfoTableClientProvider` integrates with Azure Table Storage to provide an efficient means of retrieving tenant identifiers. It's designed to work within various environments, offering fallback mechanisms to handle scenarios where tenant data might not be directly available.

## Initialization
This class is instantiated with a dependency on `ILogger<TenantInfoTableClientProvider>` for logging purposes and `IConfiguration` to access application settings, particularly for retrieving the connection string to Azure Table Storage.

Example:
```csharp
var provider = new TenantInfoTableClientProvider(logger, configuration);
```

## Methods

### GetTenantId
Attempts to retrieve the tenant ID using the specified environment and tenant key. If the data is not directly available, it initiates a process to fetch initial migration data as a fallback option.

#### Usage
```cs
string tenantId = await provider.GetTenantId(pofEnvironment, tenantIdKey);
```

#### Parameters
- `pofEnvironment`: The environment from which to retrieve the tenant ID. It influences which data partition is queried.
- `tenantIdKey`: The key for identifying the relevant tenant information.

#### Returns
A `string` representing the tenant ID.

## Utilities

### CheckTableProvisioned
Determines if the target Azure Table for tenant information is provisioned and available.

### ProvisionTable
Ensures the Azure Table is provisioned with necessary tenant information based on the provided environment.

## Exceptions
- `TableConnectionStringEmptyException`
- `NotFoundException`
- `InvalidEnvironmentException` 
are used to handle specific error scenarios within the `TenantInfoTableClientProvider` operations.

## Configuration Constants
Key application settings and constants used within this class are managed under `ConfigurationConstants`, ensuring centralized access to configuration keys and default values.
