import os ,sys 
from datetime import datetime

CURRENT_TIME_STAMP = f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"
ROOT_DIR = os.getcwd()  


CONFIG_DIR = "config"
CONFIG_FILE_NAME = "config.yaml"
CONFIG_FILE_PATH = os.path.join(ROOT_DIR , CONFIG_DIR ,CONFIG_FILE_NAME)


#Hard Coded variable related with training pipeline
TRAINING_PIPELINE_CONFIG = 'training_pipeline_config' 
TRAINING_PIPELINE_CONFIG_PIPELINE_NAME = 'pipeline_name' 
TRAINING_PIPELINE_CONFIG_ARTIFACTS_DIR = 'artifact_dir'

#VARIABLE RELATED WITH DATA INGESTION
DATA_INGESTION_CONFIG_KEY = 'data_ingestion_config'
DATA_INGESTION_DIR_KEY = 'data_ingestion_dir'
DATASET_DOWNLOAD_URL_KEY = 'dataset_download_url'
TGZ_DOWNLOAD_DIR_KEY = 'tgz_download_dir'
RAW_DATA_DIR_KEY = 'raw_data_dir'
INGESTED_DIR_KEY = 'ingested_dir'
INGESTED_TRAIN_DIR = 'ingested_train_dir'
INGESTED_TEST_DIR = 'ingested_test_dir'

#VARIABLE RELATED WITH DATA VALIDATION 
DATA_VALIDATION_CONFIG_KEY = 'data_validation_config' 
DATA_VALIDATION_DIR_KEY = 'data_validation_dir'
SCHEMA_DIR_KEY = 'schema_dir'
SCHEMA_FILE_NAME_KEY = 'schema_file_name'
REPORT_FILE_NAME_KEY = 'report_file_name'
SCHEMA_FILES_KEY = 'files'
# REPORT_FILE_NAME_KEY = 'report_file_name'
# REPORT_PAGE_FILE_NAME_KEY = 'report_page_file_name'

#VARIABLE RELATED WITH DATA TRANSFORMATION
DATA_TRANSFORMATION_CONFIG_KEY = 'data_transformation_config'
DATA_TRANSFORMATION_DIR_KEY = 'data_transformation_dir'
TOKENIZER_NAME_KEY = 'tokenizer_name'
TOKENIZER_DIR_KEY = 'tokenizer_dir' 
TOKENIZER_FILE_NAME_KEY = 'tokenizer_file_name'



#VARIABLE RELATED WITH MODEL TRAINING 
MODEL_TRAINING_CONFIG_KEY = 'model_training_config'
TRAINED_MODEL_MAIN_DIR_NAME_KEY = 'trained_model_main_dir_name' #main dir from in artifacts
TRAINED_MODEL_DIR_KEY = 'trained_model_dir'                     #Sub directory in trained_model_main_dir_name
MODEL_FILE_NAME_KEY = 'model_file_name'
TOKENIZER_DIR_KEY = 'tokenizer_dir'
TOKENIZER_FILE_NAME_KEY = 'tokenizer_file_name'
MODEL_CONFIG_DIR_KEY = 'model_config_dir' #config
MODEL_CONFIG_FILE_NAME_KEY = 'model_config_file_name' #model.yaml 


#VARIABLE RELATED WITH MODEL EVALUATION
MODEL_EVALUATION_CONFIG_KEY = 'model_evaluation_config' 
MODEL_EVALUATION_DIR_KEY = 'model_evaluation_dir' 
REPORT_FILE_NAME_KEY = 'report_file_name' 



#VARIABLE RELATED WITH MODEL PUSHING 
MODEL_PUSHER_CONFIG_KEY =  "model_pusher_config" 
EXPOSRT_DIR_NAME_KEY = "export_dir_name"
EXPORT_MODEL_FILE_NAME_KEY = "export_model_file_name"
EXPORT_TOKENIZER_FILE_NAME_KEY = "export_tokenizer_file_name"