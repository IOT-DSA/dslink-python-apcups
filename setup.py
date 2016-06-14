from setuptools import setup

setup(
    name="dslink-python-apcups",
    version="0.1.0",
    description="DSLink for APC UPSes",
    url="http://github.com/IOT-DSA/dslink-python-apcups",
    author="Logan Gorence",
    author_email="l.gorence@dglogik.com",
    license="Apache 2.0",
    install_requires=[
        "dslink == 0.6.16",
        "subprocess32 == 3.2.7"
    ]
)
