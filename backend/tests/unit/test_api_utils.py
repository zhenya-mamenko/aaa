from app.api import make_routers_list

def test_make_routers_list():
    routers = make_routers_list("v1")
    assert len(routers) != 0
    router = next(filter(lambda x: x["path"] == "", routers))
    assert router
    routers = make_routers_list("v10")
    assert len(routers) == 0
