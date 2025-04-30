from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode

# 1. Start Spark session
spark = SparkSession.builder.appName("Large JSON Structure Explorer").getOrCreate()

# 2. Path to your large JSON file
json_file_path = "../large_file.json"

# 3. Read the JSON file (without fully loading into memory)
df = spark.read.option("multiline", "true").json(json_file_path)

# 4. Show the top-level schema
print("\n=== Top-level schema ===")
df.printSchema()


# 5. Function to recursively explore nested fields
def explore_schema(schema, prefix=""):
    fields = []
    for field in schema.fields:
        name = f"{prefix}.{field.name}" if prefix else field.name
        fields.append((name, field.dataType.simpleString()))
        if "struct" in field.dataType.simpleString():
            fields += explore_schema(field.dataType, prefix=name)
        if "array" in field.dataType.simpleString():
            try:
                elementType = field.dataType.elementType
                if hasattr(elementType, "fields"):
                    fields += explore_schema(elementType, prefix=name + "[]")
            except:
                pass
    return fields


# 6. Explore full structure
schema_info = explore_schema(df.schema)

print("\n=== Full JSON Structure ===")
for path, dtype in schema_info:
    print(f"{path} : {dtype}")

# 7. Stop the Spark session
spark.stop()
