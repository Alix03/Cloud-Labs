from flask import Flask, jsonify
import math

app = Flask(__name__)

def numerical_integration(lower, upper, N):
    # Calcola la larghezza di ogni rettangolino
    dx = (upper - lower) / N
    total_area = 0.0
    
    # Somma le aree dei rettangolini
    for i in range(N):
        x = lower + (i * dx)
        # La funzione richiesta è abs(sin(x))
        y = abs(math.sin(x))
        total_area += y * dx
        
    return total_area

@app.route('/')
def home():
    return "Benvenuto! Usa /numericalintegralservice/lower/upper per calcolare."

# La rotta richiesta dal PDF: /numericalintegralservice/<lower>/<upper>
@app.route('/numericalintegralservice/<lower>/<upper>')
def integrate_service(lower, upper):
    results = {}
    
    # Il PDF chiede di testare questi valori specifici di N
    n_values = [10, 100, 1000, 10000, 100000, 1000000]
    
    for n in n_values:
        area = numerical_integration(lower, upper, n)
        results[f"N={n}"] = area
        
    # Restituisce il risultato in formato JSON
    return jsonify({
        "lower": lower,
        "upper": upper,
        "results": results
    })

if __name__ == '__main__':
    # Ascolta su tutte le interfacce (0.0.0.0) porta 5000
    app.run(host='0.0.0.0', port=5000)
