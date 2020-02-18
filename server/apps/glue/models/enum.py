from enum import Enum, unique


@unique
class DjangoChoicesEnum(Enum):

    @classmethod
    def choices(cls):
        return [(x.value, x.name.title().replace("_", " ")) for x in cls]

    @classmethod
    def values(cls):
        return [x.value for x in cls]


class RunStateEnum(DjangoChoicesEnum):
    QUEUED = 'QUEUED'
    STARTING = 'STARTING'
    RUNNING = 'RUNNING'
    STOPPING = 'STOPPING'
    STOPPED = 'STOPPED'
    SUCCEEDED = 'SUCCEEDED'
    FAILED = 'FAILED'
    TIMEOUT = 'TIMEOUT'
