# Point 5 — MapReduce with Azure Durable Functions

This project implements a serverless MapReduce framework to process text files stored in Azure Blob Storage and calculate word frequencies.

## Architecture Components

The system consists of several specialized functions coordinated by an orchestrator:
- HTTP Client Trigger (http_start): The entry point that invokes the orchestration.
- Master Orchestrator (master_orchestrator): Coordinates the workflow, managing the parallel execution of mappers and reducers.
- Get Input Data Activity (get_input_data_activity): Connects to Azure Blob Storage to retrieve the input files and split them into lines.
- Mapper Activity (mapper_activity): Tokenizes each line into <word, 1> pairs.
- Shuffler Activity (shuffler_activity): Groups the mapped results by word into <word, [1, 1, ...]>.
- Reducer Activity (reducer_activity): Aggregates the counts for each word.

## Storage Account Configuration
Account Name: lab2aliceb953a (using the account of Alice Boccadifuoco due to credit constraints).

Container: mapreduce-input (the specific container name required by the source code).

Input Files: Uploaded mrinput-1.txt, mrinput-2.txt, mrinput-3.txt, and mrinput-4.txt containing the source text.

## How to Run
**Deployment**
The function is deployed via GitHub Actions using the Azure CLI method.

**Triggering the Orchestration**
Invoke the HTTP trigger to start the process:
curl -X POST https://lab2-functions-alice-mr-final.azurewebsites.net/api/mapreduce \
  -H "Content-Type: application/json" \
  -d "{}"

**Monitoring**
Copy the statusQueryGetUri from the response.

Monitor the runtimeStatus until it reaches Completed.

The final word count results will be visible in the output field, sorted by frequency.

## Addresse of mapreduce durable function
https://lab2-functions-alice-mr-final.azurewebsites.net/api/mapreduce
