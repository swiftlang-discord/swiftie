import asyncio
import logging

from aiohttp import ClientSession

from . import config

log = logging.getLogger(__name__)


class JDoodleClient(ClientSession):
    def __init__(self):
        headers = {
            "Content-Type": "application/json",
        }
        super().__init__(headers=headers)

    async def execute(self, script: str, stdin: str = "", compile_only: bool = False):
        payload = config.JDOODLE_POST_PAYLOAD.copy()
        payload["script"] = script
        payload["stdin"] = stdin
        payload["compileOnly"] = compile_only

        retried = False

        while True:
            async with self.post(
                config.JDOODLE_EXECUTE_ENDPOINT, json=payload, timeout=30
            ) as resp:
                try:
                    resp = await resp.json()
                except Exception:
                    return

                status = resp["statusCode"]

                if status == 500 or status == 410:
                    if retried:
                        log.error(
                            "Call to JDoodle execute api resulted in an internal server error."
                        )
                        return

                    await asyncio.sleep(3)
                    retried = True
                    continue

                if status == 400:
                    log.error(
                        "Invalid request to JDoodle execute api. Payload:\n{payload}"
                    )
                    return

                if status == 401:
                    log.error("Unauthorized request to JDoodle execute api.")
                    return

                if status == 429:
                    log.warn(
                        "Daily limit for JDoodle execute requests have been reached."
                    )
                    return

                if status == 200:
                    return resp

                log.fatal(
                    f"Unexpected response from JDoodle execute api. Response:\n{resp}\nPayload:\n{payload}"
                )
                return
