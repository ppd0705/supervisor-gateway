from setuptools import setup, find_packages

with open("requirements.txt") as readme_file:
    base_requirements = readme_file.read()

with open("requirements_dev.txt") as readme_file:
    dev_requirements = readme_file.read()

setup(
    name="supervisor-gateway",
    version="0.1.0",
    author="ppd0705",
    author_email="ppd0705@icloud.com",
    description="An RESTful supervisor gateway with paginated and cached process info",
    packages=find_packages(),
    extras_require={
        "dev": dev_requirements
    },
    install_requires=base_requirements,
    classifiers=[
        "Intended Audience :: Developers",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: System :: Boot",
        "Topic :: System :: Monitoring",
        "Topic :: System :: Systems Administration",
    ],
    python_requires=">=3.7",
)
