from setuptools import setup, find_packages

setup(
    name="furniture-ner-project",
    version="1.0.0",
    author="Your Name",
    description="NER model for extracting furniture product names from websites",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "torch",
        "transformers",
        "gradio",
        "requests",
        "beautifulsoup4",
        "pandas",
    ],
)