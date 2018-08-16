#!/usr/bin/env python
import os.path
import codecs
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def readme():
    try:
        import docutils.core
    except ImportError:
        try:
            with open(os.path.join(os.path.dirname(__file__),
                      'README.rst'), 'r' ,encoding='utf-8') as f:
                return f.read()
        except (IOError, OSError):
            return ''
    with open(os.path.join(os.path.dirname(__file__), 'README.rst'), 'r' ,encoding='utf-8') as f:
        document = docutils.core.publish_doctree(f.read())
        nodes = list(document)
        description = ''
        for node in nodes:
            if str(node).startswith('<topic classes="contents"'):
                break
            if type(node) is docutils.nodes.comment \
                    or type(node) is docutils.nodes.title:
                continue
            description += node.astext() + '\n'
        return description.encode('ascii', 'ignore').strip()


setup(
    name='mlab',
    version='1.1.4',
    description='Mlab is a high-level python to Matlab bridge that lets '
                'Matlab look like a normal python library',
    long_description=readme(),
    author='Yauhen Yakimovich',
    author_email='eugeny.yakimovitch@gmail.com',
    url='https://github.com/ewiger/mlab',
    license='MIT',
    packages=['mlab'],
    package_dir={
        'mlab': 'src/mlab',
    },
    download_url='https://github.com/ewiger/mlab/tarball/master',
    # setup_requires=[
    #     'docutils >= 0.11',
    # ],
)
