from aiohttp import web
from aiohttp_xmlrpc.exceptions import ServerError

from supervisor_gateway import error
from supervisor_gateway.log import logger
from supervisor_gateway.rpc import Faults


@web.middleware
async def error_middleware(request: web.Request, handler):
    logger.debug(f"new req: {request.method} {request.url}")
    try:
        response = await handler(request)
        return response
    except ServerError as e:
        if e.code == Faults.BAD_NAME:
            err = error.ProcessNotFoundError()
        else:
            err = error.InternalError()
            logger.exception(f"{request.method} {request.url} Unknown RPCServerError.")
        return err.json_response()
    except web.HTTPException as e:
        if isinstance(e, web.HTTPNotFound):
            err = error.NotFoundError()
        elif isinstance(e, web.HTTPMethodNotAllowed):
            err = error.MethodNotAllowedError()
        else:
            err = error.InternalError()
            logger.exception(f"{request.method} {request.url} Unknown HTTPException.")
        return err.json_response()
    except:
        logger.exception(f"{request.method} {request.url} Unknown error.")
        return error.InternalError().json_response()
