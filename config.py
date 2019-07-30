from decouple import config

class Config:
	SECRET_KEY = 'codigofacilito'

class DevelopmentConfig(Config):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = 'mysql://root:alan1234@localhost/project_web'
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	MAIL_SERVER = 'smtp.googlemail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME = 'this.alan856@gmail.com'
	MAIL_PASSWORD = 'verga2282039'

class TestConfig(Config):
	SQLALCHEMY_DATABASE_URI = 'mysql://root:alan1234@localhost/project_web_test'
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	TEST = True

config = {
	'development': DevelopmentConfig,
	'default': DevelopmentConfig,
	'test': TestConfig
}