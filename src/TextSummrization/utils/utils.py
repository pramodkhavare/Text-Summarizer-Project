from src.TextSummrization.logger import logging
from src.TextSummrization.exception import TextSummarizationException
import sys ,os 
from ensure import ensure_annotations
import yaml
import numpy as np
import pandas as pd 

from box import ConfigBox 
from pathlib import Path 
from typing import Any 

@ensure_annotations
def read_yaml(yaml_file_path:str)->ConfigBox:
    try:
        """
        Read yaml file and return content as dictionary
        yaml_file_path :str
        """
        with open(yaml_file_path , 'r') as file:
            content =  yaml.safe_load(file)
            return ConfigBox(content)

    except Exception as e:
        logging.info(f'unable to read Yaml file at {yaml_file_path}')
        raise TextSummarizationException(e ,sys)
    
@ensure_annotations
def create_directories(path_to_directories:list ,verbose=True):
    try:
        """This function will create depository"""
        for path in path_to_directories:
            os.makedirs(path ,exist_ok= True)
            if verbose:
                logging.info(f"Created Directory at : {path}")

    except Exception as e:
        logging.info(f'Unable to create directory {path_to_directories}')
        raise TextSummarizationException(e ,sys)

