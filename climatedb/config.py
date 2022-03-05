from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

data_home = Path(os.environ["DATA_HOME"])
db_uri = os.environ["DB_URI"]
