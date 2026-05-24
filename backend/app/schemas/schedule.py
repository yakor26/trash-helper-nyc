from pydantic import BaseModel, ConfigDict


class ScheduleBase(BaseModel):
    days_trash: list[str]
    days_recycling: list[str]
    days_compost: list[str]
    days_large_items: list[str]

    model_config = ConfigDict(from_attributes=True)


class ScheduleResponse(ScheduleBase):
    id: int
