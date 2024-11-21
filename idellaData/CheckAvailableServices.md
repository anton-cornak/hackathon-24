# CheckAvailabilityOfDependantServices
[🖍 Diagram](diagram)

A global reusable sub-process that for checking the availability of dependent services. 
It performs a health check on each service and logs any services that are not responding successfully.
If a service is not available, it throws an exception.

##  Usage
The process can be obtained using dependency injection as a service.
It takes a `List<HealthCheckableService>`, where `HealthCheckableService` contains the URL to check.

Use `Run` or `RunAsync`:
```csharp
var services = new List<HealthCheckableService>
{
    new HealthCheckableService("http://test.com/health")
};

checkAvailabilityOfDependantServices.RunAsync(services);
```
<!-- Links -->
[diagram]: https://confluence.visma.com/pages/viewpage.action?spaceKey=VII&title=Global+Reusable+Sub-Processes+for+Execution+Models#GlobalReusableSubProcessesforExecutionModels-Checkavailabilityofdependentservices
