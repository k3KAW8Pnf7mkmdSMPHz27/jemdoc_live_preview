from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="local_jemdoc_mathjax_server",
    version="0.1.0",
    author="Jonatan Asketorp",
    author_email="jonatan.asketorp@proton.me",
    description="A local server utility for prototyping with jemdoc_mathjax",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/k3KAW8Pnf7mkmdSMPHz27/jemdoc_mathjax_experiments",
    packages=["utilities"],
    py_modules=["local_jemdoc_server"],
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: The Unlicense (Unlicense)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=[
        "Flask>=2.0.0,<3.0.0",
        "flask-socketio>=5.0.0,<6.0.0",
        "watchdog>=3.0.0,<4.0.0",
    ],
    extras_require={
        "code_style": ["black==23.9.1", "isort==5.12.0"],
    },
    entry_points={
        "console_scripts": [
            "local_jemdoc_server = local_jemdoc_server:main",
        ],
    },
)
