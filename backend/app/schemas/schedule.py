from pydantic import BaseModel, ConfigDict


class ScheduleResponse(BaseModel):
    id: int
    days_trash: dict
    days_recycling: dict
    days_compost: dict
    days_large_items: dict

    model_config = ConfigDict(from_attributes=True)
