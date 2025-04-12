import os
from pathlib import Path
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
        is_path = isinstance(file_obj, str)
        file_name = file_obj if is_path else getattr(file_obj, 'name', 'unknown_file')

        if file_type is None:
            if hasattr(file_obj, 'name'):
                file_type = file_obj.name.split('.')[-1].lower()
            elif is_path:
                file_type = Path(file_obj).suffix[1:].lower()
            else:
                raise ValueError("File type must be specified for BytesIO without a name.")
            
        if file_type not in ['csv', 'xlsx', 'xls']:
            raise ValueError(f"Unsupported file type: {file_type}. Supported types: csv, xlsx, xls")
        
        max_size_mb = 10  # Ограничение в 10 МБ
        if is_path:
            if not os.path.exists(file_obj):
                raise ValueError(f"File {file_obj} does not exist.")
            file_size_mb = os.path.getsize(file_obj) / (1024 * 1024)
        else:  # BytesIO
            file_obj.seek(0, os.SEEK_END)  # Перейти в конец файла
            file_size_bytes = file_obj.tell()  # Получить размер
            file_size_mb = file_size_bytes / (1024 * 1024)
            file_obj.seek(0)  # Вернуться в начало для чтения
        
        if file_size_mb > max_size_mb:
            raise ValueError(f"File size ({file_size_mb:.2f} MB) exceeds maximum allowed size ({max_size_mb} MB).")
        
        try:
                if file_type == 'csv':
                    df = pd.read_csv(file_obj)
                elif file_type in ['xlsx', 'xls']:
                    df = pd.read_excel(file_obj)
                
                if df.empty:
                    raise ValueError(f"File {file_name} is empty.")
                if len(df.columns) == 0:
                    raise ValueError(f"File {file_name} has no columns.")
                
        except pd.errors.EmptyDataError:
            raise ValueError(f"File {file_name} is empty or invalid.")
        except pd.errors.ParserError:
            raise ValueError(f"Unable to parse file {file_name}. Check its format.")
        except Exception as e:
            raise ValueError(f"Error reading file {file_name}: {str(e)}") 
        return df