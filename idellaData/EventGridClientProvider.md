# EventGridClientProvider

[🖍 EventGridPublisherClient](EventGridPublisherClient)
[🖍 AzureKeyCredential](AzureKeyCredential)

The `EventGridClientProvider` class serves as a factory for creating instances of `EventGridPublisherClient` configured with specific settings from an application configuration. It implements the `IEventGridClientProvider` interface to provide a method for obtaining an `EventGridPublisherClient` instance.

## Overview

This class utilizes the `IConfiguration` interface to access application settings, specifically looking for Azure EventGrid topic URI and key, which are essential for instantiating the `EventGridPublisherClient`. This approach ensures that the details required to connect to and authenticate with the Azure EventGrid service are kept external from the application code, promoting security and flexibility.


## Configuration Constants

The class depends on the following configuration constants:

- `EventGridTopicUrl`: The URL of the Azure EventGrid topic.
- `EventGridTopicKey`: The authentication key for the Azure EventGrid topic.

## Exceptions

The method `Provide` may throw a `ConfigurationErrorsException` if either the URI or the key is not found in the application's configuration settings.

<!-- Links -->
[AzureKeyCredential]: https://docs.microsoft.com/en-us/dotnet/api/azure.azurekeycredential?view=azure-dotnet
[EventGridPublisherClient]: https://docs.microsoft.com/en-us/dotnet/api/azure.messaging.eventgrid.eventgridpublisherclient?view=azure-dotnet
