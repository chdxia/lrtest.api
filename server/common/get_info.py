def get_request_info(request):
    return {
        "host": request.client.host,
        "port": request.client.port,
        "method": request.method,
        "url": request.url,
        "headers": request.headers,
        "cookies": request.cookies
    }