from setuptools import find_packages, setup

setup(
    name="dagster_movies",
    packages=find_packages(exclude=["dagster_movies_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud",
        "psycopg2-binary-2.9.6",
        "pandas-2.0.3"
    ],
    extras_require={"dev": ["dagit", "pytest"]},
)
