from rich import print
from scrapy.settings import Settings

from climatedb.database import create_newspaper_statistics, seed_newspapers

if __name__ == "__main__":
    settings = Settings()
    settings.setmodule("climatedb.settings")
    seed_newspapers(settings["DB_URI"], settings["DATA_HOME"])

    #  update newspaper article statistics
    stats = create_newspaper_statistics(settings["DB_URI"])
