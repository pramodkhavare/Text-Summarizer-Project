from dataclasses import dataclass 

@dataclass(frozen=True)
class DataIngestionArtifacts:
    ingested_data_folder_path :str
    message : str 

@dataclass(frozen=True)
class DataValidationArtifacts:
    schema_file_path :str 
    report_file_path :str 
    is_validated : bool 
    message :str

@dataclass(frozen=True)
class DataTransformationArtifacts:
    is_transformed :bool 
    message :str 
    transformed_data_folder :str 
    tokenizer_obj_file_path :str 

@dataclass(frozen=True)
class ModelTrainingArtifacts:
    trained_model_file_path :str 
    tokenizer_file_path :str

@dataclass(frozen=True)
class ModelEvaluationArtifacts:
    report_file_path :str 
    message :str 
    model_file_path :str 
    tokennizer_file_path :str

@dataclass(frozen=True)
class ModelPusherArtifacts:
    is_model_pushed :str 
    export_model_file_path :str
    export_tokenizer_file_path:str