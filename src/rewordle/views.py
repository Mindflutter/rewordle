import logging
import random

from fastapi import APIRouter, Path
from fastapi.responses import JSONResponse
from sqlalchemy.exc import NoResultFound

from db.game import Game
from rewordle.models import NOT_FOUND_RESPONSE, GuessAttemptResponse, GuessPayload, StartGameResponse

router = APIRouter(prefix="/rewordle")
logger = logging.getLogger(__name__)

WORDS = [
    "point",
    "joint",
    "yeast",
    "trust",
    "moist",
    "audio",
    "adieu",
    "weird",
    "solar",
    "clear",
    "creep",
    "creed",
    "agony",
]


@router.post("/start", status_code=201, response_model=StartGameResponse)
async def start_game():
    secret_word = random.choice(WORDS)
    result = await Game.create(secret_word)
    return result


@router.post("/guess/{game_id}", response_model=GuessAttemptResponse, responses={404: NOT_FOUND_RESPONSE})
async def guess_attempt(guess_payload: GuessPayload, game_id: int = Path(None, gt=0)):
    guess_word = guess_payload.guess_word
    if guess_word not in WORDS:
        logger.error(f"Word {guess_word} not found in the dictionary")
        return JSONResponse(status_code=404, content={"message": f"Word {guess_word} not found"})

    try:
        secret_word = await Game.process_attempt(game_id)
    except NoResultFound:
        logger.error(f"Game id {game_id} not found")
        return JSONResponse(status_code=404, content={"message": f"Game id {game_id} not found"})

    response_dict = {}
    for guess_char, secret_char in zip(guess_word, secret_word):
        if guess_char == secret_char:
            response_dict[guess_char] = "green"
        elif guess_char in secret_word:
            response_dict[guess_char] = "yellow"
        else:
            response_dict[guess_char] = "gray"

    return response_dict
