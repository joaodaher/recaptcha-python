import os

from setuptools import setup


def read_file(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

version = __import__('recaptcha', {}, {}, [''])

setup(
        name="recaptcha_python",
        version=getattr(version, '__version__', '0.0.1'),
        author="Joao Daher",
        author_email="joao.neto@stored.com.br",
        description=("Google Recaptcha v2"),
        license="BSD",
        keywords="Recaptcha",
        url="https://github.com/joaodaher/recaptcha-python",
        packages=['recaptcha-python', ],
        long_description=read_file('README.md'),
        classifiers=[
            "Topic :: Utilities",
            "License :: OSI Approved :: BSD License",
        ],
        install_requires=[
            r for r in read_file('requirements.txt').split('\n') if r],
)
