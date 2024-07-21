from streamlit import cache_data


# cache results only if kwargs supplied to function is equal to defaults
def _cache_default_factory(cache_func):

    def inner(**defaults):

        def wrapper(func):
            cached_func = cache_func(func)

            def impl(**kwargs):
                if kwargs == defaults:
                    return cached_func(**defaults)
                else:
                    return func(**kwargs)

            return impl

        return wrapper

    return inner


# can be used for things that can be stored in databases (includes go.Figure)
cache_data_default = _cache_default_factory(cache_func=cache_data(show_spinner=False))
