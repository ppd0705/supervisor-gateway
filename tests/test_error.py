from supervisor_gateway import error


def test_error():
    err = error.BaseError("HelloWorld")
    assert err.code // 100 == err.http_code
    assert err.detail == "HelloWorld"
    assert sorted(err.dict()) == sorted(["message", "code", "detail"])

    for k, v in error.__dict__.items():
        if type(v) == type and issubclass(v, error.BaseError):
            assert 400 <= v.code // 100 <= 500, "error code must be in range [400, 500]"
            assert v.message.upper() == v.message, "error message must be in all caps"
