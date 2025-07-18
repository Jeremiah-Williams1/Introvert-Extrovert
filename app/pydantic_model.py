from pydantic import BaseModel, conint, confloat
from enum import Enum

class Stage_fear(str, Enum):
    Yes ='Yes'
    No = 'No'

class features(BaseModel):
    Time_spent_Alone: int
    Social_event_attendance: int
    Going_outside: int
    Friends_circle_size: int
    Post_frequency: int
    Stage_fear: Stage_fear