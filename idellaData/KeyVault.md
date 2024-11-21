# KeyVault

The `KeyVault` class facilitates access to the `client_secret` from Azure Key Vault that's required to authenticate VIPS Pensions API requests.
It requests the key for the provided environment.

The `Environment` env variable deployed with POF processes contains one of these values: `dev`, `test`, `stage`, `prod`.
You can pass the value of this env variable directly into the service.

## Usage
Call `GetSecretAsync` to retrieve the secret:
```csharp
var environment = configuration[ConfigurationConstants.Environment];
var clientSecret = await keyVault.GetSecretAsync(environment);
```

When developing locally, you need to authenticate yourself in Visual Studio against Azure services.
