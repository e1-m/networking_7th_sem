import asyncio

import aiohttp

from src.key_generator import AesGenerator
from src.server_api import ServerApi, MessageIn
from src.session_manager import SessionManager

BASE_URL = "http://localhost:8000/api"


async def main():
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(force_close=True)) as http:
        session_manager = SessionManager(
            base_url=BASE_URL,
            http_client=http,
            key_generator=AesGenerator()
        )

        api = ServerApi(
            base_url=BASE_URL,
            http_client=http,
            session_manager=session_manager,
        )

        while True:
            msg = input("Your message (!q to quit): ")

            if msg == "!q":
                break

            server_msg = await api.echo(
                message=MessageIn(
                    message=msg,
                )
            )

            print(f"Server responded: {server_msg.message}")


if __name__ == "__main__":
    asyncio.run(main())
