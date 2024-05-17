#This code will help to convert data into necessary format
from src.TextSummrization.logger.logging import logging 
from src.TextSummrization.exception import TextSummarizationException 
from src.TextSummrization.entity.config_entity import DataTransformationConfig 
from src.TextSummrization.entity.artifacts_entity import DataIngestionArtifacts ,DataValidationArtifacts ,DataTransformationArtifacts
from src.TextSummrization.constant import *
import os ,sys 
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from datasets import load_dataset ,load_from_disk  ,load_metric

class DataTransformer():
    def __init__(self ,
                 data_transformation_config : DataTransformationConfig,
                 data_ingestion_artifacts : DataIngestionArtifacts ,
                 data_validation_artifacts : DataValidationArtifacts 
                 ):
        
        try:
            self.data_ingestion_artifacts =data_ingestion_artifacts 
            self.data_validation_artifacts = data_validation_artifacts
            self.data_transformation_config = data_transformation_config
            self.tokenizer =AutoTokenizer.from_pretrained(self.data_transformation_config.tokenizer_name)

            

        except Exception as e:
            raise TextSummarizationException(e ,sys)
        

    def convert__example_to_features(self,example_batch):
        try:
            input_encodings = self.tokenizer(example_batch['dialogue'] , max_length = 1024, truncation = True )
            with self.tokenizer.as_target_tokenizer():
                target_encodings = self.tokenizer(example_batch['summary'], max_length = 128, truncation = True )
            
            return{
                'input_ids' : input_encodings['input_ids'],
                'attention_mask': input_encodings['attention_mask'],
                'labels': target_encodings['input_ids']
                 }
        except Exception as e:
            raise TextSummarizationException(e ,sys)
        
        
    def initiated_data_transformation(self):
        try:

            # tokenizer.save_pretrained('tokenizer')

            dataset_samsun = load_from_disk(self.data_ingestion_artifacts.ingested_data_folder_path)
  
            dataset_samsun_pt = dataset_samsun.map(self.convert__example_to_features ,batched=True)
            dataset_samsun_pt.save_to_disk(self.data_transformation_config.transformed_dir )
            transformed_data_folder = self.data_transformation_config.transformed_dir 
            tokenizer_file_path = self.data_transformation_config.tokenizer_file_path
            data_transformation_artifacts = DataTransformationArtifacts(
                is_transformed= True,
                message= "Data Transformation Successfull",
                transformed_data_folder= transformed_data_folder,
                tokenizer_obj_file_path= tokenizer_file_path
            )
            # os.makedirs(self.data_transformation_config.transformed_dir ,exist_ok=True)
            # self.tokenizer.save_pretrained(tokenizer_file_path)
            return data_transformation_artifacts
        except Exception as e:
            logging.info("Unable To Apply Transformation On Data")
            raise TextSummarizationException(e ,sys)