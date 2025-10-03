from fastavro import reader

import os
from fastavro import reader
from itertools import islice

# Get the directory of this script
script_dir = os.path.dirname(__file__)

# Build the path to the .avro file located in ../dataAvro/
avro_file_path = os.path.join(script_dir, "..", "dataAvro", "53.avro")

# Normalize it (especially useful on Windows)
avro_file_path = os.path.normpath(avro_file_path)
print(avro_file_path)
# Abrir y leer el archivo .avro
with open(avro_file_path, 'rb') as file:
    avro_reader = reader(file)
    
    # Get and print schema
    schema = avro_reader.writer_schema
    print("Schema:")
    print(schema)

    print("\nFirst 3 records:")
    count = 0
    for record in avro_reader:
        print(record)
        count += 1
        if count >= 3:
            break
