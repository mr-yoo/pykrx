from setuptools import setup, find_packages

setup(
    name            = 'pykrx',
    version         = '0.0.6',
    description     = 'KRX scraping',
    url             = 'https://github.com/sharebook-kr/pykrx',
    author          = 'Brayden Jo, Lukas Yoo',
    author_email    = 'hyunho.jo@outlook.com, jonghun.yoo@outlook.com, pystock@outlook.com'
    install_requires= ['requests', 'pandas'],
    license         = 'MIT',
    packages        = find_packages(include=['pykrx', 'pykrx.*']),
    python_requires = '>=3',
    zip_safe        = False
)