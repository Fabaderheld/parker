def get_route_map(app, with_admin_routes: bool = False):
    """
    Generates a dictionary of { "route_name": "/path/{param}" }
    """
    route_map = {}
    for route in app.routes:
        # We only care about routes that have a name
        if hasattr(route, "name") and route.name:

            tags = getattr(route, "tags", [])
            if not with_admin_routes and "admin" in tags:
                continue
            route_map[route.name] = route.path

    return route_map