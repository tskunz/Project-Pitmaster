from enum import Enum


class MeatCategory(str, Enum):
    BEEF = "beef"
    PORK = "pork"
    POULTRY = "poultry"
    LAMB = "lamb"


class CutType(str, Enum):
    BRISKET = "brisket"
    PORK_BUTT = "pork_butt"
    PORK_RIBS = "pork_ribs"
    BEEF_RIBS = "beef_ribs"
    CHICKEN_WHOLE = "chicken_whole"
    TURKEY_BREAST = "turkey_breast"
    LEG_OF_LAMB = "leg_of_lamb"


class CookState(str, Enum):
    SETUP = "setup"
    PREHEAT = "preheat"
    EARLY_COOK = "early_cook"
    PRE_STALL = "pre_stall"
    STALL = "stall"
    POST_STALL = "post_stall"
    APPROACHING_TARGET = "approaching_target"
    REST = "rest"
    DONE = "done"


class ConfidenceTier(str, Enum):
    HIGH = "high"
    MODERATE = "moderate"
    LOW = "low"
    VERY_LOW = "very_low"


class EquipmentType(str, Enum):
    OFFSET = "offset"
    PELLET = "pellet"
    KAMADO = "kamado"
    WSM = "wsm"
    CUSTOM = "custom"


class WrapType(str, Enum):
    NONE = "none"
    FOIL = "foil"
    BUTCHER_PAPER = "butcher_paper"
    FOIL_BOAT = "foil_boat"


class InterventionAction(str, Enum):
    WRAP = "wrap"
    LID_OPEN = "lid_open"
    TEMP_ADJUST = "temp_adjust"


class QualityRating(str, Enum):
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
