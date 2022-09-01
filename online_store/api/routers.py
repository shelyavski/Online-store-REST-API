from rest_framework.routers import DefaultRouter, DynamicRoute, Route


class CustomApiRouter(DefaultRouter):
    def __init__(self):
        super(DefaultRouter, self).__init__()
        self.routes[1] = DynamicRoute(
            url=r'^{url_path}{trailing_slash}$',
            name='{url_name}',
            detail=False,
            initkwargs={}
        )

