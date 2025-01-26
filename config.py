import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ronald'

    MAIL_SERVER = 'sandbox.smtp.mailtrap.io'
    MAIL_PORT = 2525
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'c6e14a8d2ea340'  
    MAIL_PASSWORD = '02532fa0088a8e'  
    
    
  