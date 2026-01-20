# Point 2 — Improving Availability with VM Scale Sets

This section demonstrates how to deploy the numerical integration microservice on an Azure Virtual Machine Scale Set (VMSS) with a load balancer for high availability.

## Steps

1. **Create a VM Scale Set on Azure**

2. **Configure Each VM**

3. **Load Testing**

   - From your local machine, run Locust:
     ```
     locust -f locustfile.py --host http://<load-balancer-ip>
     ```
   - Open [http://localhost:8089](http://localhost:8089) to start the test and monitor results.

4. **Failover Test**

5. **Cleanup**

## Notes

- The microservice code is the same as in point 1.
