import zipfile
import io
import os
import pandas as pd
from pathlib import Path

zip_file_path = "./Data_set/individual+household+electric+power+consumption.zip"
output_csv_file_path = "./env/DataPreprocessing/Output_Path"
output_csv = os.path.join(output_csv_file_path, 'data_file.csv')
def convert_zip_to_csv(zip_file_path, output_csv_file_path):
    if output_csv_file_path is None:
        output_csv_file_path = Path(zip_file_path).stem+ '.csv'
    print(f"Processing zip file: {zip_file_path}")

    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                file_list = zip_ref.namelist()
                print(f"Files in zip : {file_list}")

                #find the dataset available in zip file
                data_file = None
                for file_name in file_list:
                        if file_name.endswith(('.txt','.dat','.tsv','.csv')) or '.' not in file_name:
                            data_file = file_name
                            break
                if data_file is None:
                        data_file = file_list[0]
                print(f"Processing file: {data_file}")

                temp_txt_path = Path("temp_file.txt")
                with zip_ref.open(data_file) as file_input, open(temp_txt_path, "wb") as file_output:
                       file_output.write(file_input.read())
    df = pd.read_csv(temp_txt_path, sep=';', low_memory=False)
    Path(output_csv).parent.mkdir(parents=True,exist_ok=True)
    df.to_csv(output_csv, index=False)
    print(f"CSV file saved at: {output_csv}")

def convert_csv_to_dataframe(csv_path):
                csv_file = pd.read_csv(csv_path)
                df = pd.DataFrame(csv_file)
                # return df
                print(df)


# convert_zip_to_csv(zip_file_path, output_csv_file_path)
convert_csv_to_dataframe(output_csv)
                   