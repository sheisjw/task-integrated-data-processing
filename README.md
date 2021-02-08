# task-integrated-data-processing
    .
    ├── README.md
    ├── data_processing
    │   ├── BatchManager.py
    │   ├── DataProcessingModule.py
    │   ├── docker-compose.yaml
    │   ├── process_data.py
    │   └── tag_ner.py
    ├── data_raw
    │   ├── data_iob_0911_train.txt
    ├── message_sender.ipynb
    ├── requirements.txt
    ├── research_notebooks
    │   ├── flair_ner_4_entity_model.ipynb
    │   └── weights_elmo_lstm_train_v10.ipynb
    ├── routes.py
    ├── server.py
    ├── shared_functions
    │   ├── function_a.py
    │   └── preprocess.py
    ├── tests
    │   └── test_shared_function.py
    └── text_ner_worker.py

## Step 1: train the model
Run flair_ner_4_entity_model.ipynb. Trained models, test.tsv, weights etc. will be saved in research_notebooks/flair_model folder.
Run weights_elmo_lstm_train_v10.ipynb, and trained models will be saved in research_notebooks/elmo_model folder.

## Step 2: deploy the flair model locally
Start a terminal in the root of the project and run:
>python server.py

A quick test from the terminal using cURL :
>curl --location --request POST 'http://0.0.0.0:3000/tag_ner' \
--header 'Content-Type: application/json' \
--data-raw '{"text": "Find customer with account name BMW"}'

## Step 3, run docker compose to start the kafka cluster
To build the cluster we will use a docker-compose file that will start all the docker containers needed: zookeeper and a broker.
Open a new terminal, in data_processing folder run 
>docker-compose up

## Step 4: run the Kafka producer
Module is subscribed to Kafka topic and waiting to accumulate micro-batches of 30 seconds. After window data is accumulated, send the result to the another kafka topic.  
Open a new terminal, in data_processing folder run 
>python process_data.py --broker kafka:9092 --source_topic topic_a --group_id my-group --batch_interval_seconds 30 --poll_interval_seconds 10 --target_topic=topic_b

Run message_sender.ipynb.  
Once we run the confluent_kafka_producer we should receive a log telling us that the data has been sent correctly.

## Step 5: run the Faust consumer
This consumes (makes batch prediction on) the received messages.  
Open a new terminal, in root folder run
>faust -A text_ner_worker worker -l info

## how to run unit tests?
>pytest tests/test_shared_function.py -sv