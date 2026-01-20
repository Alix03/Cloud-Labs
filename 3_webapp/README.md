# Point 3 — Scaling with Azure Web Apps

This section demonstrates how to deploy and scale the numerical integration microservice using Azure Web Apps with autoscaling enabled.

## Steps

1. **Deploy the Microservice to Azure Web App**

   - Go to the `3_webapp/` folder (contains `app.py`, `requirements.txt`, and `locustfile.py`).
   - Deploy the app to Azure Web App using VS Code, Azure CLI, or the Azure Portal.
   - After deployment, the app will be available at:
     - [https://lab2-integral-h6ayh8afgab4gaa3.italynorth-01.azurewebsites.net](https://lab2-3-afaphqdjcfhba9gm.italynorth-01.azurewebsites.net)

2. **Configure Autoscaling**

3. **Load Testing with Locust**

   - On your local machine, ensure you have Locust installed:
     ```
     pip install locust
     ```
   - From the `3_webapp/` folder, run:
     ```
     locust -f locustfile.py --host [https://lab2-integral-h6ayh8afgab4gaa3.italynorth-01.azurewebsites.net](https://lab2-3-afaphqdjcfhba9gm.italynorth-01.azurewebsites.net)

     ```
   - Open [http://localhost:8089](http://localhost:8089) in your browser, set the number of users and spawn rate, and start the test.

4. **Monitor Scaling**

5. **Stop the Web App**

## Notes

- The load test URL for Locust is:
  - [https://lab2-integral-h6ayh8afgab4gaa3.italynorth-01.azurewebsites.net](https://lab2-3-afaphqdjcfhba9gm.italynorth-01.azurewebsites.net)<img width="468" height="15" alt="image" src="https://github.com/user-attachments/assets/f3b27886-09b3-4907-a0cf-a08d4082c311" />
- Autoscaling is based on CPU usage and will automatically increase the number of instances as needed.
- Tested with the values: https://lab2-3-afaphqdjcfhba9gm.italynorth-01.azurewebsites.net/numericalintegralservice/0/3.14159
