from setuptools import find_packages, setup  # or find_namespace_packages

setup(
    packages=find_packages(),
    entry_points={'console_scripts': ['run = stl_dataset_base:build_dataset.run']}
)