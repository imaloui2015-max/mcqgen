from setuptools import setup,find_packages

setup(
    name='mcqgenerator',
    version='0.0.1',
    author='ayman imaloui',
    author_email="imaloui2015@gmail.com",
    install_requires=["google-generativeai","langchain","streamlit","python-dotenv","PyPDF2"],
    packages=find_packages()
)