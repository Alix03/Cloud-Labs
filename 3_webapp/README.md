# Point 3 — Scaling with Azure Web Apps

This section demonstrates how to deploy and scale the numerical integration microservice using Azure Web Apps with autoscaling enabled.

## Steps

1. **Deploy the Microservice to Azure Web App**

   - Go to the `3_webapp/` folder (contains `app.py`, `requirements.txt`, and `locustfile.py`).
   - Deploy the app to Azure Web App using VS Code, Azure CLI, or the Azure Portal.
   - Reference: [Azure Python Web App Quickstart](https://learn.microsoft.com/en-us/azure/app-service/quickstart-python)
   - After deployment, your app will be available at:
     - https://lab2-integral-h6ayh8afgab4gaa3.italynorth-01.azurewebsites.net

2. **Configure Autoscaling**

   - In the Azure Portal, go to your Web App → "Scale out (App Service plan)" or "Autoscale".
   - Set the rule:
     - Start with 1 instance, scale up to 3.
     - Metric: CPU Percentage > 50%
     - Time window: 1 minute.

3. **Load Testing with Locust**

   - On your local machine, ensure you have Locust installed:
     ```
     pip install locust
     ```
   - From the `3_webapp/` folder, run:
     ```
     locust -f locustfile.py --host https://lab2-integral-h6ayh8afgab4gaa3.italynorth-01.azurewebsites.net
     ```
   - Open [http://localhost:8089](http://localhost:8089) in your browser, set the number of users and spawn rate, and start the test.
   - Let Locust run for at least 3 minutes. Save the output/report for your deliverable.

4. **Monitor Scaling**

   - In the Azure Portal, use App Insights and the "Scale out" section to observe:
     - Number of instances (should increase as load grows)
     - CPU usage
     - Response times

5. **Stop the Web App**
   - After testing, stop (but do not delete) the web app from the Azure Portal.

## Notes

- The microservice code is the same as in point 1.
- The load test URL for Locust is:
  - https://lab2-integral-h6ayh8afgab4gaa3.italynorth-01.azurewebsites.net
- Autoscaling is based on CPU usage and will automatically increase the number of instances as needed.
- You can monitor all metrics and scaling events in the Azure Portal.
