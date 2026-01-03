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
    return "Welcome! Use /numericalintegralservice/lower/upper to compute."

@app.route('/numericalintegralservice/<lower>/<upper>')
def integrate_service(lower, upper):
    lower_num = float(lower)
    upper_num = float(upper)
    
    results = {}
    n_values = [10, 100, 1000, 10000, 100000, 1000000]
    
    for n in n_values:
        # Usa i numeri convertiti qui
        area = numerical_integration(lower_num, upper_num, n)
        results[f"N={n}"] = area
        
    return jsonify({
        "lower": lower_num,
        "upper": upper_num,
        "results": results
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
