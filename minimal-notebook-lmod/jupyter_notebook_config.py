import os

c.NotebookApp.ip = '*'
c.NotebookApp.port = 8080
c.NotebookApp.open_browser = False

password = os.environ.get('JUPYTER_NOTEBOOK_PASSWORD')
if password:
    import notebook.auth
    c.NotebookApp.password = notebook.auth.passwd(password)
    del password
    del os.environ['JUPYTER_NOTEBOOK_PASSWORD']

image_config_file = '/opt/app-root/src/.jupyter/jupyter_notebook_config.py'

if os.path.exists(image_config_file):
    with open(image_config_file) as fp:
        exec(compile(fp.read(), image_config_file, 'exec'), globals())

# server-proxy configuration
c.ServerProxy.servers = {
    'vscode': {
        'command': [
            'code-server',
            '--auth=none',
            '--disable-telemetry',
            '--port={port}'
        ],
        'timeout': 20,
        'launcher_entry': {
            'title': 'VS Code',
            'enabled': False
        }
    },
    'rstudio': {
        'command': [
            'rserver',
            '--www-port={port}',
            '--www-frame-origin=same',
            '--user={user}',
            '--auth-none=1',
            '--server-daemonize=0',
            '--server-working-dir=/opt/app-root/src'
        ],
        'timeout': 20,
        'absolute_url': False,
        'launcher_entry': {
            'title': 'RStudio',
            'enabled': False
        }
    },
}
