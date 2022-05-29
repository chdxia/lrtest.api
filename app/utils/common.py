class Common():
    # 获取并返回请求数据
    def get_request_info(request):
        return {
            "host": request.client.host,
            "port": request.client.port,
            "method": request.method,
            "url": request.url,
            "headers": request.headers,
            "cookies": request.cookies
        }

    # api的分页功能
    def page_to_skip(page: int, limit: int):
        if page >= 1:
            return limit*(page-1)
        else:
            return 0