# Point 1 — Numerical Integration Microservice

This microservice computes the numerical integral of the function $|\sin(x)|$ over a specified interval, using different values of N to show the convergence of the result.

## How to run

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Start the microservice:
   ```
   python app.py
   ```
3. The service will be available at `http://127.0.0.1:5000/`

## How to test

- Home page:
  - [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
- Integral calculation (example):
  - [http://127.0.0.1:5000/numericalintegralservice/0.0/3.14159](http://127.0.0.1:5000/numericalintegralservice/0.0/3.14159)

## Load test with Locust

1. Install Locust (if not already installed):
   ```
   pip install locust
   ```
2. Start Locust from the folder:
   ```
   locust -f locustfile.py --host http://127.0.0.1:5000
   ```
3. Open [http://localhost:8089](http://localhost:8089) to configure and start the test.

## Notes

- The endpoint only accepts numbers in float format (e.g. 0.0, not 0).
- The service returns results for different values of N in JSON format.
