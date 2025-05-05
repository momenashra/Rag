from prometheus_client import Counter, Histogram,generate_latest,CONTENT_TYPE_LATEST
from fastapi import Request ,Response,FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
import time


#define metrics
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total number of HTTP requests",
    ["method","endpoint","status"]
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency",
    ["method","endpoint"]
)
class PrometheusMiddleware(BaseHTTPMiddleware):
    async def dispatch(self,request:Request,call_next):
        start_time = time.time()    
        response = await call_next(request)
        duration = time.time() - start_time
        endpoint = request.url.path

        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=endpoint,
            status=response.status_code
        ).inc()
        REQUEST_LATENCY.labels(
            method=request.method,
            endpoint=endpoint
        ).observe(duration)

        return response

def setup_metrics(app:FastAPI):
    #add middleware to the app
    app.add_middleware(PrometheusMiddleware)

    #add prometheus metrics route
    @app.get("/Trythisroute",include_in_schema=False)
    
    def metrics():
        return Response(generate_latest(),media_type=CONTENT_TYPE_LATEST)
