# Point 2 — Improving Availability with VM Scale Sets

This section demonstrates how to deploy the numerical integration microservice on an Azure Virtual Machine Scale Set (VMSS) with a load balancer for high availability.

## Steps

1. **Create a VM Scale Set on Azure**

   - Go to Azure Portal → Create a resource → Virtual Machine Scale Set.
   - Choose 2 instances, Linux OS (Ubuntu recommended), and enable the load balancer.
   - Set up authentication (username/password or SSH key).

2. **Configure Each VM**

   - SSH into each VM (use the load balancer IP and port, or direct IP if available).
   - Install Python and pip if not already present.
   - Clone this repository or copy the `2_scaleset/` folder to each VM.
   - Install dependencies:
     ```
     pip install -r requirements.txt
     ```
   - Start the microservice:
     ```
     python app.py
     ```
   - (For production, consider using Gunicorn and NGINX as described in [this guide](https://krishansubudhi.github.io/webapp/2018/12/01/flaskwebapp.html)).

3. **Load Testing**

   - From your local machine, run Locust:
     ```
     locust -f locustfile.py --host http://<load-balancer-ip>
     ```
   - Open [http://localhost:8089](http://localhost:8089) to start the test and monitor results.

4. **Failover Test**

   - While Locust is running, stop one VM from the Azure Portal.
   - Observe how the load balancer redirects traffic and how Locust metrics change.

5. **Cleanup**
   - After testing, delete the VM Scale Set and all associated resources to avoid extra costs.

## Notes

- The microservice code is the same as in point 1.
- The load balancer distributes requests across both VMs.
- You can monitor VM and load balancer metrics in Azure Portal (Insights).
