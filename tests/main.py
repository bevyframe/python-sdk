from bevyframe import Frame, renderpage, request, redirect

class routes:
    def index():
        usernames = {'1234567890': 'demo'}
        username = usernames[request.cookies['session']]
        return renderpage('index.html', cuser=username, cookies=request.cookies)
    def login():
        request.cookies['session'] = '1234567890'
        return redirect('/')
    def __error_page__(error):
        return '<h1>Error Code: '+str(error)+'</h1>'

if __name__ == '__main__':
    paths = {'/': [routes.index, {}], '/login': [routes.login, {}]}
    Frame(routes, paths).start_server(host='0.0.0.0', port=8000)
