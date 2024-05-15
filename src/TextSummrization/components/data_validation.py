from src.TextSummrization.utils.utils import read_yaml 
from src.TextSummrization.config.configuration import ConfigurationManager 
from src.TextSummrization.logger.logging import logging
from src.TextSummrization.exception import TextSummarizationException 
from src.TextSummrization.entity.config_entity import DataValidationConfig
from src.TextSummrization.entity.artifacts_entity import DataIngestionArtifacts ,DataValidationArtifacts
import os,sys 



class Datavalidation():
    def __init__(self ,data_validation_config :DataValidationConfig ,
                 data_ingestion_artifacts : DataIngestionArtifacts ):
        try:
            logging.info(f'\n\n{"*" * 20} Data Validation Step Started {"*" *20}') 

            self.data_validation_config = data_validation_config 
            self.data_ingestion_artifacts = data_ingestion_artifacts 
 

        except Exception as e:
            raise TextSummarizationException(e ,sys) 
        
    def check_file_exist(self):
        try:
            logging.info('Checking Train , Test and validation file exist or not')
            os.makedirs(os.path.dirname(self.data_validation_config.status_file_path)) 
            
            ingested_data_folder_path = self.data_ingestion_artifacts.ingested_data_folder_path
            schema_file_path = self.data_validation_config.schema_file_path 
            schema_file = read_yaml(schema_file_path) 
            subfolders = list(schema_file['files'].values())  #This will give you schema(All files required)

            folders_in_dir = os.listdir(ingested_data_folder_path)  #You will get list of all files present in directory

            is_available =True
            for subfolder in subfolders:
                if subfolder not in folders_in_dir:
                    is_available  =False
                    logging.info("We Cant procees because train/test file is not available")
                    with open(self.data_validation_config.status_file_path ,'w') as file:
                        file.write(f"Validation Status : {is_available}")
                else:
                    with open(self.data_validation_config.status_file_path ,'w') as file:
                        file.write(f"Validation Status : {is_available}")
            return  is_available
        except Exception as e:
            raise TextSummarizationException(e ,sys)  
        
    def initiate_data_validation(self):
        try:
            validation_status = self.check_file_exist()
            data_validation_artifact = DataValidationArtifacts(
                schema_file_path= self.data_validation_config.schema_file_path,
                report_file_path= self.data_validation_config.status_file_path,
                is_validated= validation_status,
                message= f"We are able to validate Train and Test data successfully .Thank you Pramod Khavare"
            )
            logging.info(f"Data Validation is completed and result stored in DataValidationArtifacts [{data_validation_artifact}]")
            return data_validation_artifact

        except Exception as e:
            raise TextSummarizationException(e ,sys) 

        
    
