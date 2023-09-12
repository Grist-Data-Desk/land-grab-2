from setuptools import find_packages, setup  # or find_namespace_packages

setup(
    packages=find_packages(),
    entry_points={'console_scripts': ['run = land_activity_search:activity_match.run']}
)