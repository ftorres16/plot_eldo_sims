from setuptools import setup

setup(
    name="plot_eldo_sims",
    version="0.1",
    py_modules=["plot_eldo_sims"],
    include_package_data=True,
    install_requires=["click", "matplotlib"],
    entry_points="""
        [console_scripts]
        plot_eldo_sims=plot_eldo_sims.cli:cli
    """,
)
