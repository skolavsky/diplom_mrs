from pydantic import BaseModel, ConfigDict, Field, validator

class Data(BaseModel):#age, BMI, "1test Ex", "1test In", LF, ROX, Sp, O2 L/min
    model_config = ConfigDict(from_attributes=True)
    age: int = Field(ge=0)
    BMI: float = Field(ge=0)
    test_Ex: int = Field(ge=0, le=200)
    test_In: int = Field(ge=0, le=200)
    LF: float = Field(ge=0)
    ROX: float = Field(ge=0)
    Sp: int = Field(ge=0, le=100)
    O2: int = Field(ge=0)
    
    @validator("age")
    def validate_age(cls, value):
        if value > 100:
            return 100
        return value

if __name__ == "__main__":
    print(Data.schema())
    data = Data(age=101)
    print(data)
