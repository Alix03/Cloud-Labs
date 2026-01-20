import azure.functions as func
import azure.durable_functions as df
import json
import logging
import os
from azure.storage.blob import BlobServiceClient

app = df.DFApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# ACTIVITY FUNCTIONS

@app.activity_trigger(input_name="config")
def get_input_data_activity(config: dict):
    """
    GetInputDataFn: Reads all files from blob storage and returns [(line_num, line_text), ...]
    """
    try:
        connection_string = os.environ.get("STORAGE_CONNECTION_STRING")
        if not connection_string:
            raise ValueError("STORAGE_CONNECTION_STRING not configured")
        
        container_name = config.get("container", "mapreduce-input")
        file_names = config.get("files", ["mrinput-1.txt", "mrinput-2.txt", "mrinput-3.txt", "mrinput-4.txt"])
        
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        container_client = blob_service_client.get_container_client(container_name)
        
        lines = []
        line_num = 0
        
        for file_name in file_names:
            logging.info(f"Reading file: {file_name}")
            blob_client = container_client.get_blob_client(file_name)
            blob_data = blob_client.download_blob().readall()
            content = blob_data.decode('utf-8')
            
            for line in content.splitlines():
                if line.strip():  # Skip empty lines
                    lines.append({"key": line_num, "value": line})
                    line_num += 1
        
        logging.info(f"Loaded {len(lines)} lines from {len(file_names)} files")
        return lines
        
    except Exception as e:
        logging.error(f"Error reading from blob storage: {str(e)}")
        raise

@app.activity_trigger(input_name="line")
def mapper_activity(line: dict):
    """
    Mapper: takes (line_num, line_text) and returns [(word, 1), ...]
    """
    line_num = line.get("key")
    line_text = line.get("value", "")
    
    words = line_text.lower().split()
    result = []
    for word in words:
        word = ''.join(c for c in word if c.isalnum())
        if word:
            result.append({"key": word, "value": 1})
    
    logging.info(f"Mapper {line_num}: processed {len(words)} words")
    return result


@app.activity_trigger(input_name="map_outputs")
def shuffler_activity(map_outputs: list):
    """
    Shuffler: takes list of [(word, 1), ...] and groups by word
    Returns [(word, [1, 1, 1, ...]), ...]
    """
    shuffle_dict = {}
    
    for mapper_result in map_outputs:
        for item in mapper_result:
            word = item["key"]
            value = item["value"]
            if word not in shuffle_dict:
                shuffle_dict[word] = []
            shuffle_dict[word].append(value)
    
    result = [{"key": word, "value": values} for word, values in shuffle_dict.items()]
    
    logging.info(f"Shuffler: grouped {len(result)} unique words")
    return result


@app.activity_trigger(input_name="word_data")
def reducer_activity(word_data: dict):
    """
    Reducer: takes (word, [1, 1, 1, ...]) and returns (word, count)
    """
    word = word_data.get("key")
    values = word_data.get("value", [])
    count = sum(values)
    
    logging.info(f"Reducer: {word} = {count}")
    return {"key": word, "value": count}


# ORCHESTRATOR

@app.orchestration_trigger(context_name="context")
def master_orchestrator(context: df.DurableOrchestrationContext):
    """
    Master Orchestrator: coordinates GetInputData -> Map -> Shuffle -> Reduce
    """
    # Get input configuration (or use defaults)
    config = context.get_input() or {
        "container": "mapreduce-input",
        "files": ["mrinput-1.txt", "mrinput-2.txt", "mrinput-3.txt", "mrinput-4.txt"]
    }
    
    # Phase 0: GET INPUT DATA from blob storage
    input_lines = yield context.call_activity("get_input_data_activity", config)
    
    logging.info(f"Orchestrator: processing {len(input_lines)} lines")
    
    # Phase 1: MAP - run mappers in parallel (fan-out)
    map_tasks = []
    for line in input_lines:
        task = context.call_activity("mapper_activity", line)
        map_tasks.append(task)
    
    # Wait for all mappers to complete
    map_outputs = yield context.task_all(map_tasks)
    
    # Phase 2: SHUFFLE
    shuffle_output = yield context.call_activity("shuffler_activity", map_outputs)
    
    # Phase 3: REDUCE 
    reduce_tasks = []
    for word_data in shuffle_output:
        task = context.call_activity("reducer_activity", word_data)
        reduce_tasks.append(task)
    
    reduce_outputs = yield context.task_all(reduce_tasks)
    
    reduce_outputs.sort(key=lambda x: x["value"], reverse=True)
    
    logging.info(f"Orchestrator: completed. Total unique words: {len(reduce_outputs)}")
    
    return reduce_outputs


# HTTP CLIENT TRIGGER

@app.route(route="mapreduce")
@app.durable_client_input(client_name="client")
async def http_start(req: func.HttpRequest, client):
    # La consegna dice che l'orchestratore deve chiamare GetInputDataFn.
    # Quindi non passiamo righe di testo qui, passiamo solo la configurazione dei file (opzionale).
    instance_id = await client.start_new("master_orchestrator", client_input=None)
    return client.create_check_status_response(req, instance_id)
