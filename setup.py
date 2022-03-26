from setuptools import setup, find_packages

from supervisor_gateway import __version__

extras_require = {}
install_requires = []
with open("requirements.txt") as f:
    lines = f.readlines()
    lines = [line.strip() for line in lines if line.strip()]
    i = 0
    extra_type = ""
    for line in lines:
        if "#" == line[0]:
            extra_type = line[1:].strip("#").strip()
            extras_require[extra_type] = []
            continue
        if extra_type:
            extras_require[extra_type].append(line)
        else:
            install_requires.append(line)


def get_long_description():
    """
    Return the README.
    """
    with open("README.md", encoding="utf8") as f:
        return f.read()


setup(
    name="supervisor-gateway",
    version=__version__,
    url="https://github.com/ppd0705/supervisor-gateway",
    author="ppd0705",
    author_email="ppd0705@icloud.com",
    description="An RESTful supervisor gateway with paginated and cached process info",
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    packages=find_packages(exclude=["tests*"]),
    extras_require=extras_require,
    install_requires=install_requires,
    classifiers=[
        "Intended Audience :: Developers",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: System :: Boot",
        "Topic :: System :: Monitoring",
        "Topic :: System :: Systems Administration",
    ],
    python_requires=">=3.8",
)
