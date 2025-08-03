from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="turtle-behavior-analyzer",
    version="1.2.3",
    author="Marine Research Consortium",
    author_email="research@marinelab.org",
    description="Advanced analysis toolkit for marine turtle behavioral patterns",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/marine-research/turtle-behavior-analyzer",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Visualization",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "black>=23.0",
            "flake8>=5.0",
            "mypy>=1.0",
        ],
        "docs": [
            "sphinx>=5.0",
            "sphinx-rtd-theme>=1.0",
            "sphinx-autodoc-typehints>=1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "turtle-analyze=analyze_behavior:main",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/marine-research/turtle-behavior-analyzer/issues",
        "Source": "https://github.com/marine-research/turtle-behavior-analyzer",
        "Documentation": "https://turtle-behavior-analyzer.readthedocs.io/",
    },
)
