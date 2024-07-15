import re


def match_routing(param_str: str, path: str) -> (bool, dict):
    regex_str = param_str.replace('*', '.*')
    variables = re.findall(r'<(.*?)>', regex_str)
    for var in variables:
        regex_str = regex_str.replace(f'<{var}>', f'(?P<{var}>.*?)')
    regex_str = regex_str.replace('/', '\\/')
    regex = re.compile(f'^{regex_str}$')
    match = regex.match(path)
    if match:
        variable_values = {key: value for key, value in match.groupdict().items() if value}
        return True, variable_values
    else:
        return False, {}