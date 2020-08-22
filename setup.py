import setuptools

setuptools.setup(
    name='easy_json',
    version='1.0',
    author='Nickolai Beloguzov',
    author_email='nickolai.beloguzov@gmail.com',
    packages=['easy_json'],
    install_requires = [
        'jsonpath_ng'
    ],
    entry_points = {
        'easy_json': ['easy_json=easy_json.utils'] 
    }
)
