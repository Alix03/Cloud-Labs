import azure.functions as func
import math
import time

app = func.FunctionApp()

def numerical_integral(a, b, n):
    dx = (b - a) / n
    total = 0.0
    x = a
    for _ in range(n):
        total += abs(math.sin(x)) * dx
        x += dx
    return total

@app.function_name(name="numericalintegral")
@app.route(route="numericalintegral", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)
def numericalintegral(req: func.HttpRequest) -> func.HttpResponse:
    try:
        a = float(req.params.get("a"))
        b = float(req.params.get("b"))
    except:
        return func.HttpResponse(
            "Missing or invalid parameters a and b",
            status_code=400
        )

    results = {}
    for n in [10, 100, 1000, 10000]:
        start = time.time()
        val = numerical_integral(a, b, n)
        elapsed = time.time() - start
        results[n] = {
            "value": val,
            "time": elapsed
        }

    return func.HttpResponse(
        body=str(results),
        mimetype="application/json",
        status_code=200
    )
