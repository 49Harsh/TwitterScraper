from setuptools import setup, find_packages

setup(
    name="twitter_scraper",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        line.strip()
        for line in open("requirements.txt")
        if not line.startswith("#")
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A Twitter trend scraper with proxy rotation and MongoDB storage",
    keywords="twitter, scraping, selenium, mongodb",
    python_requires=">=3.8",
)
