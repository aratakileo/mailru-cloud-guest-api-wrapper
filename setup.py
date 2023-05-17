try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='mailru_cloud_guest_api',
    version='1.0.0',
    packages=['mailru_cloud_guest_api'],
    url='https://github.com/teacondemns/mailru-cloud-guest-api-wrapper',
    license='MIT',
    author='Tea Condemns',
    author_email='tea.condemns@gmail.com',
    description='Non-official wrapper API for mail.ru cloud designed to generate a link or links to a file stream '
                'via a public link, for example to download file as a guest'
)
