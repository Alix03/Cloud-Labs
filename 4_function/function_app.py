import azure.functions as func
import logging
import math

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="calculate_integral")
def calculate_integral(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Computing integral...')
    try:
        a = float(req.params.get('a'))
        b = float(req.params.get('b'))
        n = int(req.params.get('n', 10000))

        def f(x):
            return abs(math.sin(x))

        h = (b - a) / n
        result = 0.5 * (f(a) + f(b))
        for i in range(1, n):
            result += f(a + i * h)
        result *= h

        return func.HttpResponse(f"{result}", status_code=200)
    except Exception as e:
        return func.HttpResponse("Error: provide a, b, n", status_code=400)