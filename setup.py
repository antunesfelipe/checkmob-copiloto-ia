from setuptools import setup, find_packages

setup(
    name="checkmob_copiloto",
    version="0.1",
    packages=find_packages(include=[
        "checkmob_copiloto*",
        "onyx*",
        "ee*",
        "onyx.redis*",
        "shared_configs*",
        "model_server*",
        "alembic*",
        "alembic_tenants*",
        "scripts*",
        "tests*",             # se for importar testes ou rodar via setup
    ]),
    package_dir={"": "."},
    include_package_data=True,
)
