from typing import Optional

from pydantic import BaseModel, Field, validator


class GuessPayload(BaseModel):
    guess_word: str = Field(title="An attempt guess word", min_length=5, max_length=10)


class StartGameResponse(BaseModel):
    game_id: int = Field(title="Game id", gt=0)


class GuessAttemptResponse(BaseModel):
    __root__: dict[str, str]

    # TODO: add validator
    @validator("__root__")
    def check_dict(cls, input_dict):
        # print(input_dict)
        return input_dict


class ErrorResponse(BaseModel):
    message: str


NOT_FOUND_RESPONSE = {
    "model": ErrorResponse,
    "description": "Returned when word was not found in the dictionary or game id was not found in the database",
}
DUPLICATE_RESPONSE = {"model": ErrorResponse, "description": "Item already exists"}
