from setuptools import setup, find_packages

setup(
    name="checkmob_copiloto",
    version="0.1",
    packages=find_packages(where="backend", include=[
        "checkmob_copiloto*", "onyx*", "ee*", "onyx.redis*", "shared_configs*"
    ]),
    package_dir={"": "backend"},
    include_package_data=True,
)

