
from dataclasses import dataclass 

@dataclass
class Version:
    version_nbr:str
    version_endpoint:str

version_1 = Version("v1.0", "/v1")

version_list = [
    version_1
]

def versions():
    return version_list