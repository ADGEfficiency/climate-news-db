from pathlib import Path
import os
from dotenv import load_dotenv

from dotenv import dotenv_values

de = dotenv_values()

data_home = os.environ.get("DATA_HOME", de["DATA_HOME"])
s3_prefix = os.environ.get("S3_PREFIX", de["S3_PREFIX"])
db_uri = os.environ.get("DB_URI", de["DB_URI"])
s3_bucket = de["S3_BUCKET"]
region = de["AWSREGION"]
