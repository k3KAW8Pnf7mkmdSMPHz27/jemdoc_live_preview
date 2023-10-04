from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="jemdoc_mathjax_local_server",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A local server utility for prototyping with jemdoc_mathjax",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your_github_username/jemdoc_mathjax_local_server",
    packages=["jemdoc_mathjax_local_server"],
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: The Unlicense (Unlicense)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
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
            "jemdoc_mathjax_server=jemdoc_mathjax_local_server.jemdoc_mathjax_local_server:main",
        ],
    },
)
