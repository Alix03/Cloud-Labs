import time
from locust import HttpUser, task, between

class AzureFunctionUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def calculate_integral(self):
        # Test of Azure Function
        self.client.get("/api/calculate_integral?a=0.0&b=3.14159&n=10000")
