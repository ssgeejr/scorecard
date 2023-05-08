import sys

from AutomateJiraTicketing import JiraEngine
from TethysCore import DataEngine

if __name__ == "__main__":
    data_engine = DataEngine()
    data_engine.main(*sys.argv[1:])
    files = data_engine.fetchFileStack()
    for dates in files:
        engine = JiraEngine(dates)
        engine.fetchSQLData()
