from dataclasses import dataclass 

@dataclass(frozen=True)
class DataIngestionArtifacts:
    ingested_data_folder_path :str
    message : str 