from enum import Enum

class WorkMode(str, Enum):
    REMOTE = "FullRemote"
    HYBRID = "Hybrid"
    ON_SITE = "Onsite"

