import azure.functions as func
import math
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="calculate_integral", methods=["GET"])
def calculate_integral(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # Recupero parametri dalla URL
        a = float(req.params.get('a'))
        b = float(req.params.get('b'))
        n = int(req.params.get('n', 10000)) # Default a 10.000 se manca

        # Logica del calcolo dell'integrale (|sin(x)|)
        h = (b - a) / n
        def f(x): return abs(math.sin(x))
        
        # Regola del trapezio
        result = 0.5 * (f(a) + f(b))
        for i in range(1, n):
            result += f(a + i * h)
        result *= h

        return func.HttpResponse(
            body=json.dumps({"result": result, "n": n}),
            mimetype="application/json",
            status_code=200
        )
    except (TypeError, ValueError):
        return func.HttpResponse("Pass parameters a, b and n", status_code=400)
