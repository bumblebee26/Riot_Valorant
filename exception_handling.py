import requests
import time

def get_response(method, URL, parameters):
    error_txt = {
        400: 'Bad request',
        401: 'Unauthorized',
        403: 'Forbidden',
        404: 'Data not found',
        405: 'Method not allowed',
        415: 'Unsupported media type',
        429: 'Rate limit exceeded',
        500: 'Internal server error',
        502: 'Bad gateway',
        503: 'Service unavailable',
        504: 'Gateway timeout'
    }

    res = requests.request(method, URL, headers=parameters)
    status_code = res.status_code
    if status_code == 200:
        return res.content
    
    elif status_code == 429:
        time.sleep(5)
        print(f'Retrying as API response is {status_code} : {error_txt[status_code]}')
        return get_response(method, URL, parameters)

    elif status_code in [400, 401, 403, 404, 405, 415, 500, 502, 503, 504]:
        raise Exception(f'{status_code} : {error_txt[status_code]}')
    
    else:
        raise Exception(f'Unknown Exception found : {status_code}')