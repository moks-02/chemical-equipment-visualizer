import pandas as pd
import numpy as np
import io


def parse_csv_file(file):
    """
    Parse uploaded CSV file and return DataFrame.
    
    Args:
        file: Uploaded file object
        
    Returns:
        pandas.DataFrame: Parsed data
        
    Raises:
        ValueError: If CSV is invalid or missing required columns
    """
    try:
        # Read CSV file
        df = pd.read_csv(file)
        
        # Required columns
        required_columns = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
        
        # Check if all required columns exist
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")
        
        # Validate numeric columns
        numeric_columns = ['Flowrate', 'Pressure', 'Temperature']
        for col in numeric_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Drop rows with any NaN values in numeric columns
        df = df.dropna(subset=numeric_columns)
        
        if len(df) == 0:
            raise ValueError("No valid data rows found after cleaning")
        
        return df
    
    except pd.errors.EmptyDataError:
        raise ValueError("CSV file is empty")
    except pd.errors.ParserError:
        raise ValueError("Invalid CSV format")
    except Exception as e:
        raise ValueError(f"Error parsing CSV: {str(e)}")


def calculate_summary(df):
    """
    Calculate summary statistics from DataFrame.
    
    Args:
        df: pandas.DataFrame with equipment data
        
    Returns:
        dict: Summary statistics including:
            - total_count: Total number of equipment
            - avg_flowrate: Average flowrate
            - avg_pressure: Average pressure
            - avg_temperature: Average temperature
            - equipment_type_distribution: Count of each equipment type
            - min/max values for numeric fields
    """
    summary = {
        'total_equipment': int(len(df)),
        'total_types': int(df['Type'].nunique()),
        'total_count': int(len(df)),
        'avg_flowrate': float(round(df['Flowrate'].mean(), 2)),
        'avg_pressure': float(round(df['Pressure'].mean(), 2)),
        'avg_temperature': float(round(df['Temperature'].mean(), 2)),
        'min_flowrate': float(round(df['Flowrate'].min(), 2)),
        'max_flowrate': float(round(df['Flowrate'].max(), 2)),
        'min_pressure': float(round(df['Pressure'].min(), 2)),
        'max_pressure': float(round(df['Pressure'].max(), 2)),
        'min_temperature': float(round(df['Temperature'].min(), 2)),
        'max_temperature': float(round(df['Temperature'].max(), 2)),
        'equipment_type_distribution': {str(k): int(v) for k, v in df['Type'].value_counts().to_dict().items()},
        'type_distribution': {str(k): int(v) for k, v in df['Type'].value_counts().to_dict().items()},  # Alias for frontend
    }
    
    return summary


def dataframe_to_json(df):
    """
    Convert DataFrame to JSON-serializable list of dictionaries.
    
    Args:
        df: pandas.DataFrame
        
    Returns:
        list: List of dictionaries representing each row
    """
    # Convert DataFrame to records and ensure all numpy types are converted to Python types
    records = df.to_dict(orient='records')
    
    # Convert numpy types to Python native types
    for record in records:
        for key, value in record.items():
            if isinstance(value, (np.integer, np.int64)):
                record[key] = int(value)
            elif isinstance(value, (np.floating, np.float64)):
                record[key] = float(value)
            elif pd.isna(value):
                record[key] = None
    
    return records
