import azure.functions as func
import azure.durable_functions as df
import math
import os
from azure.storage.blob import BlobServiceClient

# Usiamo DFApp per supportare sia le funzioni standard che quelle Durable
app = df.DFApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# 4
@app.route(route="calculate_integral")
def calculate_integral(req: func.HttpRequest) -> func.HttpResponse:
    try:
        a, b = float(req.params.get('a')), float(req.params.get('b'))
        n = int(req.params.get('n', 10000))
        f = lambda x: abs(math.sin(x))
        h = (b - a) / n
        res = 0.5 * (f(a) + f(b)) + sum(f(a + i * h) for i in range(1, n))
        return func.HttpResponse(f"{res * h}", status_code=200)
    except:
        return func.HttpResponse("Error: check params a, b, n", status_code=400)

# 5: MapReduce Durable Function
@app.route(route="mapreduce_start")
@app.durable_client_input(client_name="client")
async def http_start(req: func.HttpRequest, client):
    instance_id = await client.start_new("MasterOrchestrator", None)
    return client.create_check_status_response(req, instance_id)

@app.orchestration_trigger(context_name="context")
def MasterOrchestrator(context: df.DurableOrchestrationContext):
    # 1. Get Data
    input_data = yield context.call_activity("GetInputDataFn", None)
    # 2. Map (Parallel)
    map_tasks = [context.call_activity("Mapper", line) for line in input_data]
    map_results = yield context.task_all(map_tasks)
    # 3. Shuffle
    shuffled = yield context.call_activity("Shuffler", map_results)
    # 4. Reduce (Parallel)
    reduce_tasks = [context.call_activity("Reducer", item) for item in shuffled]
    return yield context.task_all(reduce_tasks)

@app.activity_trigger(input_name="line")
def Mapper(line):
    # Tokenize and produce <word, 1>
    return [(w.lower(), 1) for w in line["value"].split()]

@app.activity_trigger(input_name="payload")
def Reducer(payload):
    # Sum counts for a word
    return {payload["key"]: sum(payload["value"])}

@app.activity_trigger(input_name="unused")
def GetInputDataFn(unused):
    # Legge dal blob store usando connection string
    conn = os.environ.get("STORAGE_CONNECTION_STRING")
    client = BlobServiceClient.from_connection_string(conn)
    container = client.get_container_client("mapreduce-input")
    data = []
    for blob in container.list_blobs():
        content = container.get_blob_client(blob).download_blob().readall().decode('utf-8')
        for i, line in enumerate(content.splitlines()):
            data.append({"key": i, "value": line})
    return data

@app.activity_trigger(input_name="map_results")
def Shuffler(map_results):
    temp = {}
    for task in map_results:
        for word, count in task:
            temp.setdefault(word, []).append(count)
    return [{"key": k, "value": v} for k, v in temp.items()]
