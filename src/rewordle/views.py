import logging
import random

from fastapi import APIRouter, Path
from fastapi.responses import JSONResponse
from sqlalchemy.exc import NoResultFound

from db.game import Game
from rewordle.models import NOT_FOUND_RESPONSE, GuessAttemptResponse, GuessPayload, StartGameResponse
from rewordle.utils import generate_response
from settings import WORDS

router = APIRouter(prefix="/rewordle")
logger = logging.getLogger(__name__)


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

    response_list = generate_response(guess_word, secret_word)
    return response_list
