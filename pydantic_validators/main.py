from datetime import date, datetime
from pydantic import BaseModel, validator, create_model


def date_to_datetime_val(cls, value):
    print("validator")
    return datetime.strptime(value, '%Y-%m-%d')


Model = create_model('Model', date_val=(datetime, ...), datetime_val=(datetime, ...), __validators__={
    '__date_val_validator': validator('date_val', pre=True)(date_to_datetime_val)
})


if __name__ == "__main__":

    js = """{
        "date_val": "2019-07-11",
        "datetime_val": "2019-07-11T12:40:52"
    } """

    instance = Model.parse_raw(js)

    print(instance.dict())