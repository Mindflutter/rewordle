from pydantic import BaseModel, Field, validator


class GuessPayload(BaseModel):
    guess_word: str = Field(title="An attempt guess word", min_length=5, max_length=10)

    @validator("guess_word")
    def check_guess_word(cls, value):
        if not all([value.isalpha(), value.islower()]):
            raise ValueError("Only lowercase letters allowed")
        return value


class StartGameResponse(BaseModel):
    game_id: int = Field(title="Game id", gt=0)


class GuessAttemptResponse(BaseModel):
    __root__: list[str]

    # TODO: add validator
    @validator("__root__")
    def check_attempt_response(cls, input_list):
        return input_list


class ErrorResponse(BaseModel):
    message: str


NOT_FOUND_RESPONSE = {
    "model": ErrorResponse,
    "description": "Returned when word was not found in the dictionary or game id was not found in the database",
}
