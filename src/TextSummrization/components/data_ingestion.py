from src.TextSummrization.logger.logging import logging 
from src.TextSummrization.exception import TextSummarizationException 
from src.TextSummrization.constant import CONFIG_FILE_PATH
from src.TextSummrization.config.configuration import DataIngestionConfig
from src.TextSummrization.entity.artifacts_entity import DataIngestionArtifacts


import os ,sys 
import urllib.request as request
import os 
from pathlib import Path 
import shutil
from six.moves import urllib
import tarfile
import pandas as pd
import zipfile

class DataIngestion:
    def __init__(self ,data_ingestion_config : DataIngestionConfig):
        try:
            logging.info(f"\n\n{'*'*20}Data Ingestion Step Started{'*'*20}")
            self.config = data_ingestion_config 
        except Exception as e:
            raise TextSummarizationException(e ,sys)
        
    def download_file(self):
        """
        This function will help you to download data from online source in .zip format
        """
        try:
            # os.makedirs(self.config.tgz_download_dir ,exist_ok=True)
            if  os.path.exists(self.config.tgz_download_dir) :
                shutil.rmtree(self.config.tgz_download_dir) 
            os.makedirs(self.config.tgz_download_dir ,exist_ok=True)

            text_summ_file_name = os.path.basename(self.config.dataset_download_url)
            tgz_file_path = os.path.join(self.config.tgz_download_dir ,text_summ_file_name)
            logging.info(f"Downloading Data at file: [{tgz_file_path}]  from url: [{self.config.dataset_download_url}]")

            filename ,url =urllib.request.urlretrieve(
                url= self.config.dataset_download_url ,
                filename = tgz_file_path
            )
            logging.info(f"File : [{tgz_file_path}] has been downloaded successfully")

            return tgz_file_path

        except Exception as e:
            logging.info(f"Unable to download file from given URL")
            raise TextSummarizationException(e ,sys)
    

    def extract_tgz_file(self ,tgz_file_path):
        try:
            logging.info('Unzipping Downloaded File ')
            if os.path.exists(self.config.raw_data_dir):
                 shutil.rmtree(self.config.raw_data_dir) 
            
            os.makedirs(self.config.raw_data_dir ,exist_ok=True)

            logging.info(f"Unziping data into [{self.config.raw_data_dir}]")

            with zipfile.ZipFile(tgz_file_path ,'r') as text_data_tgz_file_obj:
                text_data_tgz_file_obj.extractall(path=self.config.raw_data_dir)

        except Exception as e:
            logging.info(f"Unable to unzip given file")
            raise TextSummarizationException(e ,sys)
    

    # def get_final_data(self):
    #     try:
    #         raw_data_dir = self.config.raw_data_dir 
    #         ingested_data_dir = self.config.ingested_dir 
    #         os.makedirs(ingested_data_dir ,exist_ok=True)
    #         final_data_dir = [item for item in os.listdir(raw_data_dir) if os.path.isdir(os.path.join(raw_data_dir, item))][0]
    #         print(final_data_dir)

    #         text_summarization_data_repo_path = os.path.join(raw_data_dir ,final_data_dir)
    #         source_subdir_path = text_summarization_data_repo_path 
    #         destination_subdir_path = ingested_data_dir

    #         subdirectories = [subdir for subdir in os.listdir(text_summarization_data_repo_path)]


    #         for subdir in subdirectories:
    #             source_subdir_path = os.path.join(text_summarization_data_repo_path, subdir)
    #             destination_subdir_path = os.path.join(ingested_data_dir, subdir)
                
    #             if os.path.isfile(source_subdir_path):
    #                 print(source_subdir_path)
    #                 shutil.copy(source_subdir_path, destination_subdir_path)
    #             elif os.path.isdir(source_subdir_path):
    #                 if not os.path.exists(source_subdir_path):
    #                     os.makedirs(source_subdir_path)
    #                 shutil.copytree(source_subdir_path, destination_subdir_path)


    #         logging.info(f"Copied All Files at : {self.config.ingested_dir}")

    #         data_ingestion_artifacts = DataIngestionArtifacts(
    #             ingested_data_folder_path= destination_subdir_path,
    #             message= f"Data Ingestion is completed"
    #         )

    #         return data_ingestion_artifacts

        # except Exception as e:
        #     logging.info(f"Unable to get Train test validation file")
        #     raise TextSummarizationException(e ,sys)
    

    def get_final_data(self):
        try:
        
            raw_data_dir = self.config.raw_data_dir 
            ingested_data_dir = self.config.ingested_dir 
            os.makedirs(ingested_data_dir, exist_ok=True)

            final_data_dir = [item for item in os.listdir(raw_data_dir) if os.path.isdir(os.path.join(raw_data_dir, item))][0]
  

            text_summarization_data_repo_path = os.path.join(raw_data_dir, final_data_dir)

            for root, _, files in os.walk(text_summarization_data_repo_path):
                for file in files:
                    source_file_path = os.path.join(root, file)
                    destination_file_path = os.path.join(ingested_data_dir, os.path.relpath(root, text_summarization_data_repo_path), file)
                    os.makedirs(os.path.dirname(destination_file_path), exist_ok=True)
                
                # Check if the file already exists in the destination directory
                    if os.path.exists(destination_file_path):
                        # If the file already exists, overwrite it
                        shutil.copy(source_file_path, destination_file_path)
                    else:
                        shutil.copy(source_file_path, destination_file_path)
            logging.info(f"Copied All Files at : {self.config.ingested_dir}")

            data_ingestion_artifacts = DataIngestionArtifacts(
                ingested_data_folder_path= ingested_data_dir,
                message= f"Data Ingestion is completed"
            )

            return data_ingestion_artifacts


        except Exception as e:
            logging.info(f"Unable to initiated data ingestion")
            raise TextSummarizationException(e ,sys)
        
    def initiate_data_ingestion(self) ->DataIngestionArtifacts:
        try:
            tgz_file_path = self.download_file()
            self.extract_tgz_file(tgz_file_path=tgz_file_path)
            data_ingestion_artifacts = self.get_final_data()

            logging.info(f"{'*'*20}Data Ingestion Step Completed{'*'*20}")

            return data_ingestion_artifacts 
        except Exception as e:
            logging.info(f"Unable to Initiate Data Ingestion step")
            raise TextSummarizationException(e ,sys)