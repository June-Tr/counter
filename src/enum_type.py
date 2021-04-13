from enum import Enum


class counter_type(Enum):
    WORK = 1
    REST = 2


class termination_status(Enum):
    """
    Keep track if a method is terminate by themself. or a call from another method
    """
    # ended by themself
    SUCCESS = 0

    # Another method terminated
    INTERRUPT = 1
