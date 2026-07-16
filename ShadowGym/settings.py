MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'members.middleware.LoginRequiredMiddleware',  # <-- agregar
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'  # cambia por el nombre real de tu vista principal
LOGOUT_REDIRECT_URL = 'login'