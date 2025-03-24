import pandas as pd
from io import BytesIO
from typing import Union

class FileService:
    @staticmethod
    def read_dataframe(file_obj: Union[BytesIO, str], file_type: str = None) -> pd.DataFrame:
        """
        Reads a file and returns a DataFrame
        
        Args:
            file_obj: File object or file path
            file_type: File type (csv, xlsx). If None, determined by file name
            
        Returns:
            pd.DataFrame: The read DataFrame
        """
        if file_type is None and hasattr(file_obj, 'name'):
            file_type = file_obj.name.split('.')[-1].lower()
        
        if file_type == 'csv':
            return pd.read_csv(file_obj)
        elif file_type in ['xlsx', 'xls']:
            return pd.read_excel(file_obj)
        else:
            raise ValueError(f"Unsupported file type: {file_type}") 
        