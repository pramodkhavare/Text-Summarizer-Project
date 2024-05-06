from src.TextSummrization.entity.config_entity import DataIngestionConfig ,TrainingPipelineConfig
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
                self.training_pipeline_config ,
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

            logging.info("Data ingestion config step completed")
            return data_ingestion_config
        except TextSummarizationException as e:
            raise TextSummarizationException(e ,sys)

    def get_training_pipeline_config(self) ->TrainingPipelineConfig:
        try:
            config = self.config_info[TRAINING_PIPELINE_CONFIG]
            artifact_dir  = os.path.join(ROOT_DIR 
                                         ,config[TRAINING_PIPELINE_CONFIG_ARTIFACTS_DIR])
            
            training_pipeline_config = TrainingPipelineConfig(artifact_dir=artifact_dir)
            return training_pipeline_config.artifact_dir

        except Exception as e:
            raise TextSummarizationException (e ,sys)
        


if __name__ == '__main__':
    manager = ConfigurationManager(
        config_file_path= CONFIG_FILE_PATH ,
        current_time_stamp= CURRENT_TIME_STAMP
    )
    print(manager.get_data_ingestion_config())

# "src\TextSummrization\config\configuration.py"