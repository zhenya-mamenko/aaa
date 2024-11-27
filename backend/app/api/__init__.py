def make_routers_list(api_version: str) -> list[dict]:
    """
    Generate a list of routers for the specified API version.

    Args:
        api_version (str): The version of the API to generate routers for.

    Returns:
        list[dict]: A list of dictionaries, each containing the path and router object.
    """

    from importlib import import_module
    from os import path, walk

    try:
        m = import_module(f"app.api.{api_version}.endpoints")
    except ImportError:
        return []

    filenames = [m for m in map(lambda x: ".".join(x.split(".")[:-1]),
        next(walk(path.dirname(m.__file__)), (None, None, []))[2]
    )]
    routers_list = []
    for filename in filenames:
        m = import_module(f"app.api.{api_version}.endpoints.{filename}")
        if not m or not hasattr(m, "router"):
            continue
        router = {
            "path": f"/{filename}" if not hasattr(m, "router_path") else m.router_path,
            "router": m.router,
        }
        routers_list.append(router)

    return routers_list
