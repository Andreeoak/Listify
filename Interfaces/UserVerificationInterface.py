from pydantic import BaseModel, Field, field_validator
import phonenumbers
from phonenumbers.phonenumberutil import NumberParseException

class UserPasswordVerificationInterface(BaseModel):
    password: str
    new_password: str = Field(min_length=6)
     
    
class UserPhoneVerificationInterface(BaseModel):
    new_phone: str

    @field_validator("new_phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        try:
            parsed_number = phonenumbers.parse(v, None)
            if not phonenumbers.is_valid_number(parsed_number):
                raise ValueError("Invalid phone number")
        except NumberParseException:
            raise ValueError("Invalid phone number format")
        # Return the formatted E.164 version
        return phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)