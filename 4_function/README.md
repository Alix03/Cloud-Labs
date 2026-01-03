# Point 4 — Scaling Microservice with Azure Functions

This section demonstrates how to deploy the numerical integration logic as an Azure Function and test its autoscaling capabilities.

## Steps

1. **Deploy the Function to Azure**

   - Go to the `4_function/` folder (contains `function_app.py`, `requirements.txt`, and `locustfile_functions.py`).
   - Use VS Code, Azure CLI, or the Azure Portal to deploy the function to Azure Functions.
   - Reference: [Azure Functions Python Quickstart](https://learn.microsoft.com/en-us/azure/azure-functions/create-first-function-vs-code-python?pivots=python-mode-configuration)
   - After deployment, note your function URL (e.g., https://<your-function-app>.azurewebsites.net/api/calculate_integral).

2. **Configure Autoscaling**

   - Azure Functions on the Consumption Plan scale automatically based on demand.
   - You can set the maximum number of instances (default is 200) in the Azure Portal if needed.

3. **Load Testing with Locust**

   - On your local machine, ensure you have Locust installed:
     ```
     pip install locust
     ```
   - From the `4_function/` folder, run:
     ```
     locust -f locustfile_functions.py --host https://<your-function-app>.azurewebsites.net
     ```
   - Open [http://localhost:8089](http://localhost:8089) in your browser, set the number of users and spawn rate, and start the test.
   - Let Locust run for at least 3 minutes. Save the output/report for your deliverable.

4. **Monitor Scaling**

   - In the Azure Portal, use App Insights and the Function App metrics to observe:
     - Number of function instances
     - Execution count
     - Response times

5. **Stop the Function**
   - After testing, you can stop the Function App from the Azure Portal (do not delete it).

## Notes

- The function implements the same numerical integration logic as in previous points.
- The load test URL for Locust is your Azure Function endpoint ([e.g., https://<your-function-app>.azurewebsites.net](https://integral-func.azurewebsites.net)).
- Azure Functions scale automatically; you do not need to configure a load balancer or VM.
- You can monitor all metrics and scaling events in the Azure Portal.
