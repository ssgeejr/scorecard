from dataclasses import dataclass
import os, configparser, time

@dataclass
class Config:
    dtkey: str = time.strftime('%m%y')
    userDefinedKey: bool = False
    configFile: str = 'db.ini'
    working_dir: str = '/opt/apps/sc.data'
    cdir: str = os.path.dirname(os.path.abspath(__file__))
    user_id: str = ''