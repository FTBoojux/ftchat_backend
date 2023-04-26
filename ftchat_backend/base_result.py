def success(data):
    result = Result
    result.code = 200
    result.message = 'success'
    result.data = data
    return result


def fail(data):
    result = Result
    result.code = 201
    result.message = 'fail'
    result.data = data
    return result


class Result:

    def __init__(self):
        self.code = 500
        self.message = 'fail'
        self.data = None
