from dataclasses import dataclass
from typing import Dict, Any, Optional

from utils.log_control import write_log, LogType

@dataclass
class JobClassify:
    PhysicalDisability: bool
    BrainLesion: bool
    VisualImpairment: bool
    HearingImpairment: bool
    SpeechDisorder: bool
    FacialDeformity: bool
    KidneyDisorder: bool
    CardiacDisorder: bool
    LiverDisorder: bool
    RespiratoryDisorder: bool
    UrinaryDiversion: bool
    Epilepsy: bool
    IntellectualDisability: bool
    Autism: bool
    MentalIllness: bool