from bevyframe import *


def load_info(context: Context) -> change_html:
    return change_html('div#info', [
        Title(f'Hello, {context.user.id.name} {context.user.id.surname} from {context.user.network}!'),
        Label(f"You are using {context.browser.device}"),
        Label(
            f"You are using {context.browser.name} {context.browser.version} which uses WebKit {context.browser.webkit_version}"),
        Label(f"Your browser's language is set to {context.browser.language}"),
        Label(f"Your device has {context.browser.ram} GB of RAM"),
        Label(f"Your bandwith is {context.browser.bandwidth} Mbps"),
        Label(f"Your network type is {context.browser.network_profile}"),
        Label(f"Your last visited profile is {context.last_visited_profile}"),
    ])