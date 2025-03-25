def login_required(func) -> callable:
    def wrapper(r, *args, **kwargs) -> any:
        if r.username == 'Guest':
            return r.start_redirect(f"/{r.loginview.removeprefix('/')}")
        else:
            return func(r, *args, **kwargs)
    return wrapper
