import os ,sys 
from datetime import datetime 
from dataclasses import dataclass 
from pathlib import Path 

def get_time_stamp():
    return datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

@dataclass(frozen=True)
class TrainingPipelineConfig:
    artifacts_dir :str 

@dataclass(frozen=True)
class DataIngestionConfig:
    dataset_download_url :str
    tgz_download_dir : str 
    raw_data_dir :str
    ingested_dir :str 
    ingested_train_dir :str 
    ingested_test_dir :str

@dataclass(frozen=True)
class DataValidationConfig:
    schema_file_path : str 
    # report_file_path : Path 
    # report_page_file_path : Path 
    status_file_path : str 

@dataclass(frozen=True)
class DataTransformationConfig:
    transformed_dir :str 
    tokenizer_dir_path :str 
    tokenizer_file_path : str 
    tokenizer_name :str
    

@dataclass(frozen=True)
class ModelTrainingConfig:
    trained_model_folder_path :str
    trained_model_file_path: str 
    model_config_file_path :str 
    tokenizer_file_path : str

@dataclass(frozen=True)
class ModelEvaluationConfig:
    model_evalution_dir :str
    report_file_path :str 


@dataclass(frozen=True)
class TrainingPipelineConfig:
    artifact_dir :str