# BevyFrame 0.5 ɑ

Python Web Framework that turns your Python scripts to a web page.
With decentralized features integrated, it makes programming easier than ever.

***Alpha version, yet to guarantee backwards compatibility***

## Features

- **WSGI compatible,** use your favorite WSGI server on production
- **Fast development server,** built directly on sockets
- **Serving Python scripts as a web pages,** thanks to the widget based templating¹
- **Python based styling,** no need to use CSS²
- **Rich request and response objects** for easy development³
- **Built-in decentralized authentication** with [TheProtocols](https://github.com/islekcaganmert/TheProtocols)
- **Decentralized db-less user data** with [TheProtocols](https://github.com/islekcaganmert/TheProtocols)
- **Decentralized user querying** with [TheProtocols](https://github.com/islekcaganmert/TheProtocols)
- **Powerful built-in routing engine** that lets you combine static routing and dynamic overwrites⁴
- **Customizable logging** with built-in logging engine
- **Built-in error handling** customizable with a single file⁵
- **Built-in web debugger** for easy debugging
- **Page Authorization** with blacklist or whitelist⁶
- **Multiple apps in a single project,** just end your package name with a dot

<small>
1. Widgets are rendered to the HTML, it doesn't require any additional client-side code.<br>
2. CSS can be combined with the style scripts or directly used. Style scripts are compiled to CSS.<br>
3. Unnecessary arguments can be disabled to speed up the project.<br>
4. Since static routing is default, no private data should be in working directory.<br>
5. To customize, create Python script with error code as name.<br>
6. TheProtocols is required.
</small>

## Installations

pymake
```bash
# Latest development version
pymake install islekcaganmert/bevyframe@dev
# Latest release
pymake install bevyframe
```

PyPI
```bash
# Latest development version
pip install git+https://github.com/islekcaganmert/bevyframe@dev
# Latest release
pip install bevyframe
```

Wheel
```bash
pip install https://github.com/islekcaganmert/bevyframe/releases/download/0.5/BevyFrame-0.5.0-py3-none-any.whl
```

<small>*now included in LuOS developer tools</small>

## Links
- Documentation: https://bevyframe.islekcaganmert.me/
- Source Code: https://github.com/islekcaganmert/bevyframe
- Issue Tracker: https://github.com/islekcaganmert/bevyframe/issues
- Fediverse Tag: [#bevyframe](https://mastodon.social/tags/bevyframe)
- X Hashtag: [#bevyframe](https://x.com/search?q=%23bevyframe)
- Reddit: [r/bevyframe](https://www.reddit.com/r/bevyframe)
- Lemmy: [!bevyframe@lemmy.today](https://lemmy.today/c/bevyframe)
- Discord: *Soon*
