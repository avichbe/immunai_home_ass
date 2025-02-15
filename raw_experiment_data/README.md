# Single Cell Biological Analysis Data Engineering Assignment

We are interested in understanding patterns from single cell biological analysis data. Your task is to construct a small data pipeline that processes a JSON file of single cell experiments and addresses a particular hypothesis based on this data.

Each experimental entry is of this form:
```json
{
    "date": "2018-01-21T00:00:00.000Z",
    "cell_type": {
        "id": 2,
        "name": "Neuron",
        "location": "Brain",
        "function": "Signal processing"
    },
    "environment": {
        "id": 22,
        "name": "In vivo",
        "condition": "Healthy",
        "medium": "Blood",
        "temperature": "37°C"
    },
    "cell_response": 8.5,
    "duration": 120,
    "treatment": "Drug A",
    "status": "Completed"
}
```

# Assignment:
## Hypothesis:
**Neurons have a higher response in "In vivo" environments compared to other cell types on average.**<br>
_In vivo: biological term for 'in a living body of an animal'_<br>

You have been designated to share your knowledgeable stance on the hypothesis's validity, deriving insights from real experimental data.<br>
For this, you will design a small data pipeline encompassing 3 stages, utilizing the filesystem for uncomplicated data exchanges.<br>

## Pipeline data exchange: files on local disk
Each step of the assigment is a small "data pipeline", the input to each pipeline should be passed as a file on the local disk, and the output would be a file on the local disk.<br>
**Each "data pipeline" should be triggered by a new file appearing in a specific directory**, and should output a file to another specific directory (which in turn will trigger the next "data pipeline").<br>

(We are saving the intermediary outputs, so that we have a record of our data processing)<br>
The execution of each "data pipeline" should be asynchronous - it should be possible to have multiple "data pipelines" running at the same time.<br>


## Step 1: Generate a raw data file using the experiment ID
**Input:** a data file in the `raw_experiment_data/` directory with `[EXPERIMENT_ID].json` as its filename, containing the JSON list of the experiment data.<br>
**Output:** a data file with the `[EXPERIMENT_ID].json` as its filename.<br>
Extract only the relevant data to assess the hypothesis for the specified experiment from the JSON list within the file.<br>
(We are limited in our disk space, so we want to avoid saving unnecessary data)
 

## Step 2: Validate the hypothesis per experiment
**Input:** Output from step 1.<br>
**Output:** a data file with the `[EXPERIMENT_ID].json` as its filename.<br>
Determine the validity of the hypothesis for this specific experiment.


## Step 3: Validate the hypothesis across all the processed experiments
**Input:** Outputs from step 2.<br>
**Output:** Print of `hypothesis is true for: [FLOAT]%`.<br>
Compile a summary on the hypothesis's accuracy % for all the experiments that have been processed up until now.


## How to test your code
We have provided you with data to test your code. You may copy it to your `raw_experiment_data/` directory.<br>
This data should trigger a run of your code, and you should see the output of **Step 3** printed to the console.


## Important notes
* You are expected to do the assignment on your own, and we will expect you to explain your code and design decisions.
* Limit yourself to 3 hours of work, and try your best in that time.
* Make sure your code works.
* Make the code as production-worthy as possible, we want to see your coding style and abilities.
* Consider good coding design and practices along the way (e.g. OOP, SOLID).
