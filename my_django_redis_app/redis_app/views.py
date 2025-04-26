from django.shortcuts import render
from django.core.cache import cache


def redis_view(request):
    key = 'my_test_key'
    value_to_set = 'Hello from Django with Redis Cloud!'
    timeout = 60 * 5 # 5 minutes

    set_success = False
    set_error = None
    get_success = False
    get_error = None
    retrieved_value = None

    try:
        cache.set(key, value_to_set, timeout=timeout)
        set_success = True
    except Exception as e:
        set_success = False
        set_error = str(e)

    try:
        retrieved_value = cache.get(key)
        get_success = True
    except Exception as e:
        get_success = False
        get_error = str(e)
        retrieved_value = None

    context = {
        'key': key,
        'value_to_set': value_to_set,
        'timeout': timeout,
        'set_success': set_success,
        'set_error': set_error,
        'get_success': get_success,
        'get_error': get_error,
        'retrieved_value': retrieved_value,
    }

    return render(request, 'redis_app/index.html', context)