from src.TextSummrization.entity.config_entity import DataIngestionConfig ,DataValidationConfig,TrainingPipelineConfig,DataTransformationConfig ,ModelTrainingConfig,ModelEvaluationConfig ,ModelPusherConfig
from src.TextSummrization.entity.artifacts_entity import DataIngestionArtifacts
from src.TextSummrization.exception import TextSummarizationException 
from src.TextSummrization.logger.logging import logging 
from src.TextSummrization.constant import *
from src.TextSummrization.utils.utils import read_yaml 

class ConfigurationManager:
    """
    This class will help us to get required configuration for all methods like data_ingestion ,data_validation 
    
    """
    def __init__(self ,
                #  config:DataIngestionConfig ,
                 config_file_path = CONFIG_FILE_PATH ,
                 current_time_stamp = CURRENT_TIME_STAMP):
        try:
            # self.config = config  
            self.config_file_path = config_file_path
            self.current_time_stamp = current_time_stamp 
            self.config_info = read_yaml(self.config_file_path)
            self.training_pipeline_config = self.get_training_pipeline_config()
        except Exception as e:
            raise TextSummarizationException(e ,sys)
        
    def get_data_ingestion_config(self)->DataIngestionConfig:
        try:
            config = self.config_info[DATA_INGESTION_CONFIG_KEY]
            data_ingestion_dir_key = os.path.join(
                self.training_pipeline_config.artifact_dir ,
                config[DATA_INGESTION_DIR_KEY] ,
                self.current_time_stamp
            )

            tgz_download_dir = os.path.join(
                data_ingestion_dir_key ,
                config[TGZ_DOWNLOAD_DIR_KEY]
            )

            raw_data_dir = os.path.join(
                data_ingestion_dir_key ,
                config[RAW_DATA_DIR_KEY]
            )

            ingested_dir = os.path.join(
                data_ingestion_dir_key ,
                config[INGESTED_DIR_KEY]
            )

            ingested_train_dir = os.path.join(
                data_ingestion_dir_key ,
                config[INGESTED_TRAIN_DIR]
            )

            ingested_test_dir = os.path.join(
                data_ingestion_dir_key ,
                config[INGESTED_TEST_DIR]
            )

            dataset_download_url = config[DATASET_DOWNLOAD_URL_KEY]


            data_ingestion_config = DataIngestionConfig(
                dataset_download_url= dataset_download_url,
                tgz_download_dir= tgz_download_dir,
                raw_data_dir= raw_data_dir,
                ingested_dir= ingested_dir,
                ingested_train_dir= ingested_train_dir,
                ingested_test_dir= ingested_test_dir
            ) 
            return data_ingestion_config
        except TextSummarizationException as e:
            raise TextSummarizationException(e ,sys)
        
    def get_data_validation_config(self) -> DataValidationConfig:
        try:
            config = self.config_info[DATA_VALIDATION_CONFIG_KEY] 

            data_validation_dir_key = os.path.join(
                self.training_pipeline_config.artifact_dir ,
                config[DATA_VALIDATION_DIR_KEY] ,
                self.current_time_stamp 
            )
            schema_file_path = os.path.join(
                ROOT_DIR ,
                config[SCHEMA_DIR_KEY] ,
                config[SCHEMA_FILE_NAME_KEY]
            )

            status_file_path = os.path.join(
                data_validation_dir_key ,
                config[REPORT_FILE_NAME_KEY]
            )

            data_validation_config = DataValidationConfig(
                schema_file_path= schema_file_path,
                status_file_path= status_file_path
            )

            return data_validation_config

        except Exception as e:
            raise TextSummarizationException (e ,sys)

    def get_data_transformation_config(self) ->DataTransformationConfig:
        try:
            logging.info("Getting Data Transformation Config Component")
            config =self.config_info[DATA_TRANSFORMATION_CONFIG_KEY] 
            transformed_dir = os.path.join(
                self.training_pipeline_config.artifact_dir ,
                config[DATA_TRANSFORMATION_DIR_KEY] ,
                self.current_time_stamp
            )

            tokenizer_dir_path = os.path.join(
                transformed_dir ,
                config[TOKENIZER_DIR_KEY])
            
            tokenizer_file_path = os.path.join(
                transformed_dir ,
                config[TOKENIZER_DIR_KEY] ,
                config[TOKENIZER_FILE_NAME_KEY] )

            tokenizer_name = config[TOKENIZER_NAME_KEY]
            data_transformation_config = DataTransformationConfig(
                transformed_dir= transformed_dir,
                tokenizer_dir_path= tokenizer_dir_path,
                tokenizer_file_path= tokenizer_file_path ,
                tokenizer_name= tokenizer_name
            )


            return data_transformation_config
        except TextSummarizationException as e:
            raise TextSummarizationException(e ,sys)
        
    def get_model_training_config(self)->ModelTrainingConfig:
        try:
            config = self.config_info[MODEL_TRAINING_CONFIG_KEY]
            trained_model_folder_path =  os.path.join(
                self.training_pipeline_config.artifact_dir ,
                config[TRAINED_MODEL_MAIN_DIR_NAME_KEY] ,
                self.current_time_stamp 
            )
            trained_model_file_path =  os.path.join(
                trained_model_folder_path ,
                config[MODEL_FILE_NAME_KEY]
                
            )
            model_config_file_path = os.path.join(
                ROOT_DIR ,
                config[MODEL_CONFIG_DIR_KEY] ,
                config[MODEL_CONFIG_FILE_NAME_KEY]
            )
            
            tokenizer_file_path = os.path.join(
                self.training_pipeline_config.artifact_dir ,
                config[TRAINED_MODEL_MAIN_DIR_NAME_KEY] ,
                self.current_time_stamp ,
                config[TOKENIZER_FILE_NAME_KEY]

            )
            model_training_config = ModelTrainingConfig(
                trained_model_folder_path = trained_model_folder_path ,
                trained_model_file_path= trained_model_file_path, 
                model_config_file_path= model_config_file_path ,
                tokenizer_file_path= tokenizer_file_path
            )
            return model_training_config

        except TextSummarizationException as e:
            raise TextSummarizationException(e ,sys)
        

    def get_training_pipeline_config(self) ->TrainingPipelineConfig:

        try:
            config = self.config_info[TRAINING_PIPELINE_CONFIG]
            artifact_dir  = os.path.join(ROOT_DIR 
                                         ,config[TRAINING_PIPELINE_CONFIG_ARTIFACTS_DIR])
            
            training_pipeline_config = TrainingPipelineConfig(artifact_dir=artifact_dir)
            return training_pipeline_config

        except Exception as e:
            raise TextSummarizationException (e ,sys)
    def get_model_evaluation_config(self) -> ModelEvaluationConfig:
        try:
            config =self.config_info[MODEL_EVALUATION_CONFIG_KEY]

            model_evaluation_dir_key = os.path.join(
                self.training_pipeline_config.artifact_dir ,
                config[MODEL_EVALUATION_DIR_KEY] ,
                self.current_time_stamp 
            )
            report_file_path = os.path.join(
                model_evaluation_dir_key,
                config[REPORT_FILE_NAME_KEY]
            )
            
            model_evaluation_config = ModelEvaluationConfig( 
                model_evalution_dir= model_evaluation_dir_key ,
                report_file_path= report_file_path
            )

            return model_evaluation_config
        except Exception as e:
            raise TextSummarizationException (e ,sys) 
        
    def get_model_pusher_config(self) ->ModelPusherConfig:
        try:
            config = self.config_info[MODEL_PUSHER_CONFIG_KEY] 

            dir_name = config[EXPOSRT_DIR_NAME_KEY]
            export_dir_path = os.path.join(
                ROOT_DIR ,
                dir_name ,
                CURRENT_TIME_STAMP
            )

            export_file_path = os.path.join(
                export_dir_path ,
                config[EXPORT_MODEL_FILE_NAME_KEY]
            )

            export_tokenizer_file_path = os.path.join(
                export_dir_path ,
                config[EXPORT_TOKENIZER_FILE_NAME_KEY]
            )

 
            model_pusher_config = ModelPusherConfig(
                export_dir_path= export_dir_path,
                export_model_file_path= export_file_path ,
                export_tokenizer_file_path = export_tokenizer_file_path
            )
            return model_pusher_config

        except Exception as e:
            raise TextSummarizationException (e ,sys) 


if __name__ == '__main__':
    manager = ConfigurationManager(
        config_file_path= CONFIG_FILE_PATH ,
        current_time_stamp= CURRENT_TIME_STAMP
    )

# "src\TextSummrization\config\configuration.py"