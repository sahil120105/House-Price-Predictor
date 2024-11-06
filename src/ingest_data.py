import os
import zipfile
from abc import ABC, abstractmethod
import pandas as pd


#Define an abstract class for DataIngestor
class DataIngestor(ABC):
    @abstractmethod
    def ingest(self, file_path:str) -> pd.DataFrame:
        """Abstract method to ingest data from a given file"""
        pass


#Implement concrete class for zip ingestion
class ZipDataIngestor(DataIngestor):
    def ingest(self, file_path:str) -> pd.DataFrame:
        """Extracts a .zip file and returns a pandas dataframe"""

        #ensure file is a .zip
        if not file_path.endswith(".zip"):
            raise ValueError("The provided file is not a .zip file")
        
        #extract the zip file
        with zipfile.ZipFile(file_path, "r") as zip_ref:
            zip_ref.extractall("D:\ML Projects\House Price Prediction\extracted_data")

        #find the extracted csv file (assuming there is only one csv file in the .zip file)
        extracted_files = os.listdir("extracted_data")
        csv_files = [f for f in extracted_files if f.endswith(".csv")]

        if len(csv_files) == 0:
            raise FileNotFoundError("No CSV file found in extracted_data")
        if len(csv_files) > 1:
            raise ValueError("Multiple CSV files found. Specify which one to use")
        
        #read the CSV into a dataframe
        csv_file_path = os.path.join("D:\ML Projects\House Price Prediction\extracted_data", csv_files[0])
        df = pd.read_csv(csv_file_path)

        #return the dataframe
        return df
    

#Implement a Factory to create DataIngestors
class DataIngestorFactory:
    @staticmethod
    def get_data_ingestor(file_extension: str) -> DataIngestor:
        """Returns the appropriate data ingestor based on the file extension"""

        if file_extension == ".zip":
            return ZipDataIngestor()
        else:
            raise ValueError(f"No ingestor available for file extension: {file_extension}")
        

if __name__ == "__main__":
    
    #specify file path
    file_path =  "D:\ML Projects\House Price Prediction\data/archive.zip"

    #determine file extension
    file_ext = os.path.splitext(file_path)[1]

    #get appropriate data ingestor
    data_ingestor = DataIngestorFactory.get_data_ingestor(file_ext)

    #ingest the data and load it into dataframe
    df = data_ingestor.ingest(file_path)

    #display the first few rows of the dataframe
    print(df.head())