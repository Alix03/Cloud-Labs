# Point 4 — Scaling Microservice with Azure Functions

This section demonstrates how to deploy the numerical integration logic as an Azure Function and test its autoscaling capabilities.

## Steps

1. **Deploy the Function to Azure**

   - Go to the `4_function/` folder (contains `function_app.py`, `requirements.txt`, and `locustfile_functions.py`).
   - Use VS Code, Azure CLI, or the Azure Portal to deploy the function to Azure Functions.
   - After deployment, note the function URL (e.g., [https://<your-function-app>.azurewebsites.net/api/calculate_integral](https://lab2-functions-alice-byd5hkfaeea9evga.italynorth-01.azurewebsites.net/api/calculate_integral)).


2. **Configure Autoscaling**

3. **Load Testing with Locust**

   - On your local machine, ensure you have Locust installed:
     ```
     pip install locust
     ```
   - From the `4_function/` folder, run:
     ```
     locust -f locustfile_functions.py --host [https://<your-function-app>.azurewebsites.net](https://lab2-functions-alice-byd5hkfaeea9evga.italynorth-01.azurewebsites.net/api/calculate_integral)

     ```
   - Open [http://localhost:8089](http://localhost:8089) in your browser, set the number of users and spawn rate, and start the test.

4. **Monitor Scaling**
5. 
6. **Stop the Function**

## Notes

- The function implements the same numerical integration logic as in previous points.
- The load test URL for Locust is the Azure Function endpoint ([[e.g., https://<your-function-app>.azurewebsites.net](https://integral-func.azurewebsites.net)](https://lab2-functions-alice-byd5hkfaeea9evga.italynorth-01.azurewebsites.net/api/calculate_integral)).
- Tested with values: https://lab2-functions-alice-byd5hkfaeea9evga.italynorth-01.azurewebsites.net/api/calculate_integral?a=0&b=3.14159&n=10000
 
