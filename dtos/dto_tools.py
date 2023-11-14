from dataclasses import dataclass
import dataclasses
import json

def dataclass_to_json(dataclass: object) -> str:
    return json.dumps(dataclasses.asdict(dataclass))
    
