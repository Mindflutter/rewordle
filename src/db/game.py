from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, SmallInteger, String, select, update

from db.database import db
from db.model_base import Base
from rewordle.models import StartGameResponse


class Game(Base):
    __tablename__ = "game"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    # leave room for longer words
    word = Column(String(10), nullable=False)
    attempts = Column(SmallInteger, default=0, nullable=False)
    start_time = Column(DateTime, default=datetime.utcnow, nullable=False)

    @classmethod
    async def check_game_exists(cls, session, game_id):
        # check if a game exists in the db
        check_query = select(1).where(Game.id == game_id)
        results = await session.execute(check_query)
        # NoResultFound will be raised here if a game with a given id does not exist
        results.one()

    @classmethod
    async def create(cls, word: str):
        game = Game(word=word)
        async with db.session_maker() as session:
            session.add(game)
            await session.commit()
        return StartGameResponse(game_id=game.id)

    @classmethod
    async def process_attempt(cls, game_id: int):
        async with db.session_maker() as session:
            await cls.check_game_exists(session, game_id)

            # get secret word, update attempts counter
            query = update(Game).where(Game.id == game_id).values(attempts=Game.attempts + 1).returning(Game.word)
            results = await session.execute(query)
            (result,) = results.one()
            await session.commit()
            return result
