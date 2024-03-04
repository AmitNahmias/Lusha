import datetime
from typing import Dict

import asyncpg
from asyncpg import Pool
from fastapi import FastAPI, HTTPException, Query
from starlette.responses import JSONResponse

from conf import DB_CONF, DB_NAME
from logger import setup_logger

app = FastAPI()
LOGGER = setup_logger(__name__)


# Database connection pool
async def _get_pool() -> Pool:
    return await asyncpg.create_pool(user=DB_CONF["user"], password=DB_CONF["password"],
                                     database=DB_NAME, host='localhost')


def _clean_phone_number(phone_number: str) -> str:
    return ''.join([char for char in phone_number if char.isdigit()])


# Function to execute the query
async def _fetch_caller_id(phone_number: str) -> str | None:
    """
    Search for the phone number in the DB

    :param phone_number: The phone number to search for
    :return: Phone number if found.
    """
    LOGGER.info(f'Searching for {phone_number =}')

    pool = await _get_pool()
    LOGGER.debug('Created pool')
    clean_phone_number: str = _clean_phone_number(phone_number)

    # validate that the number is in appropriate length and not None
    if not clean_phone_number or len(clean_phone_number) > 15 or len(clean_phone_number) < 7:
        return None

    async with pool.acquire() as connection:
        query = f"""
            SELECT parsed_name
            FROM {DB_CONF['schema']}.{DB_CONF['table']}
            WHERE parsed_phone_number = $1
            GROUP BY parsed_name
            ORDER BY COUNT(*) DESC, MIN(score)
            LIMIT 1;
        """
        return await connection.fetchval(query, clean_phone_number)


@app.get("/caller_id")
async def get_caller_id(phone_number: str = Query(..., alias="phone")) -> Dict:
    LOGGER.info(f'Got {phone_number =}')
    caller_info: str = await _fetch_caller_id(phone_number)
    if caller_info:
        LOGGER.info(f'Found {caller_info =}')
        return \
            {
                "full_name": caller_info
            }
    else:
        LOGGER.warning(f'There is no match for {phone_number =} in our data :(')
        raise HTTPException(status_code=404, detail=f"Caller ID {phone_number =} not found")


@app.get("/")
async def is_alive() -> Dict:
    return \
        {
            'time': datetime.datetime.now(),
            'status': True
        }


# Custom middleware to handle unsupported query parameters
@app.middleware("http")
async def check_query_params(request, call_next) -> JSONResponse:
    expected_params = ["phone", "phone_number"]  # Add any other supported parameter names here
    for param in request.query_params.keys():
        if param not in expected_params:
            return JSONResponse(status_code=400, content={"Error": f" '{param}' is not a supported parameter"})
    response = await call_next(request)
    return response
