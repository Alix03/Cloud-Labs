import time
from locust import HttpUser, task, between

class QuickstartUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def hello_world(self):
        # local server
        self.client.get("/numericalintegralservice/0.0/3.14159")

        #point to http://localhost:5000
