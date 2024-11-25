token_required_code_map = {
    "0401": "invalid token",
    "0402": "expired token",
    "0403": "forbidden"
}

get_token_code_map = {
    200: "Ok",
    400: "Bad request",
    401: "Unauthorized",
    403: "Forbiden",
    500: "Internal error"
}

token_expiration_in_minutes = 30