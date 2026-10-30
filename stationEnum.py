from enum import IntEnum

class Station(IntEnum):
    ALLOCATIONS    = 1
    BAY_DROPS      = 2
    PURCHASING     = 3
    RECEIVING      = 4
    CREATE_NEST    = 5
    NESTING        = 6
    HOLZMA         = 7
    EDGING         = 8
    HINGING        = 9
    REWORKS_QA     = 10
    REWORK_COMPLETE = 11
    DISPATCH       = 12
    TROLLEY_SPECIALS = 15
    TROLLEY_CUTDOWN  = 16
    TROLLEY_JOB      = 17
    RAPID_COMPLETE   = 99

class Reason(IntEnum):
    MISSING                   = 1
    CHIPPED                   = 2
    SCRATCHED                 = 3
    BOWED                     = 4
    EDGE_MISSING              = 5
    EDGE_FALLING_OFF          = 6
    EDGE_SHORT                = 7
    EDGE_WRONG_COLOUR         = 8
    EDGE_WRONG_SIDE           = 9
    GLUE_LUMPS                = 10
    ALLOCATIONS_NOT_IN_TROLLEY = 11
    MDF_3MM_MISSING           = 12
    PARTICLE_BOARD_16MM_MISSING = 13
    MDF_16MM_MISSING          = 14
    WRONG_SIZE                = 15
    NOT_SQUARE                = 16
    EDGE_RUN_OFF              = 17
    EDGE_SCRATCHED            = 18
    EDGE_CRACKING             = 19
    STICKER_WRONG             = 20
    GRAIN_MATCH               = 21

class Tool(IntEnum):
    SAW = 1
    CNC = 2
