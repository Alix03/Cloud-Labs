from flask import Flask, jsonify
import math

app = Flask(__name__)

def numerical_integration(lower, upper, N):
    dx = (upper - lower) / N
    total_area = 0.0
    
    for i in range(N):
        x = lower + (i * dx)
        # La funzione richiesta è abs(sin(x))
        y = abs(math.sin(x))
        total_area += y * dx
        
    return total_area

@app.route('/')
def home():
    return "Benvenuto! Usa /numericalintegralservice/lower/upper per calcolare."

@app.route('/numericalintegralservice/<float:lower>/<float:upper>')
def integrate_service(lower, upper):
    results = {}
    
    n_values = [10, 100, 1000, 10000, 100000, 1000000]
    
    for n in n_values:
        area = numerical_integration(lower, upper, n)
        results[f"N={n}"] = area
        
    return jsonify({
        "lower": lower,
        "upper": upper,
        "results": results
    })

if __name__ == '__main__':
    # Ascolta su tutte le interfacce (0.0.0.0) porta 5000
    app.run(host='0.0.0.0', port=5000)
