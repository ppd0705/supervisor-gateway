from asyncio import get_event_loop

from aiohttp_xmlrpc.exceptions import ServerError as RPCServerError
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST
from starlette.status import HTTP_404_NOT_FOUND
from starlette.status import HTTP_405_METHOD_NOT_ALLOWED

from supervisor_gateway.api.local import router as local_router
from supervisor_gateway.api.rpc import router as rpc_router
from supervisor_gateway.error import BadRequestError
from supervisor_gateway.error import InternalError
from supervisor_gateway.error import InvalidParameterError
from supervisor_gateway.error import MethodNotAllowedError
from supervisor_gateway.error import NotFoundError
from supervisor_gateway.error import ProcessNotFoundError
from supervisor_gateway.log import logger
from supervisor_gateway.supervisor import Faults


def get_app() -> FastAPI:
    app_ = FastAPI()
    app_.include_router(local_router, tags=["local"])
    app_.include_router(rpc_router, prefix="/rpc", tags=["rpc"])
    return app_


app = get_app()


@app.on_event("startup")
async def on_startup():
    from supervisor_gateway.event_listener import listener
    from supervisor_gateway.local_state import state
    from supervisor_gateway.xml_rpc import rpc

    rpc.init_client()

    supervisor_state = await rpc.get_state()
    state.update_supervisor(supervisor_state["statename"])
    process_list = await rpc.get_all_process_info()
    state.add_processes(process_list)

    listener.set_handler(state.event_handler)
    loop = get_event_loop()
    task = loop.create_task(listener.start())
    app._listener_task = task

    def _clean_task():
        app._listener_task = None

    task.add_done_callback(_clean_task)
    logger.debug("on_startup finished")


@app.on_event("shutdown")
async def on_shutdown():
    from supervisor_gateway.event_listener import listener
    from supervisor_gateway.xml_rpc import rpc

    listener.stop()
    await rpc.close()
    logger.debug("on_shutdown finished")


@app.exception_handler(RPCServerError)
async def xml_rpc_exception_handler(request: Request, exc: RPCServerError):
    if exc.code == Faults.BAD_NAME:
        err = ProcessNotFoundError()
    else:
        err = InternalError()
        logger.exception(f"{request.method} {request.url} got XMLServerError.")
    return JSONResponse(
        status_code=err.http_code,
        content=err.dict(),
    )


@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(
    request: Request, exc: RequestValidationError
):
    err = InvalidParameterError(exc.errors())
    return JSONResponse(
        status_code=err.http_code,
        content=err.dict(),
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == HTTP_400_BAD_REQUEST:
        err = BadRequestError(exc.detail)
    elif exc.status_code == HTTP_404_NOT_FOUND:
        err = NotFoundError(exc.detail)
    elif exc.status_code == HTTP_405_METHOD_NOT_ALLOWED:
        err = MethodNotAllowedError(exc.detail)
    else:
        logger.exception(f"{request.method} {request.url} got unknown error.")
        err = InternalError()
    return JSONResponse(
        status_code=err.http_code,
        content=err.dict(),
    )
