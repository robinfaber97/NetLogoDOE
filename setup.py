from distutils.core import setup
setup(
  name = 'NetLogoDOE',
  packages = ['NetLogoDOE'],
  version = '0.1.7',
  license='MIT',
  description = 'NetLogoDOE provides a GUI that allows for easy design, execution and analysis of NetLogo experiments',
  author = 'Robin Faber',
  author_email = 'r.j.faber@student.tudelft.nl',
  url = 'https://github.com/robinfaber97/NetLogoDOE',
  download_url = 'https://github.com/robinfaber97/NetLogoDOE/archive/refs/tags/0.1.7.tar.gz',
  keywords = ['NetLogo', 'Design of experiments', 'Model design', 'Agent-based simulation', 'Data visualisation'],
  install_requires=[
          'PySimpleGUI',
          'plotly',
          'statsmodels',
          'pandas',
          'pyNetLogo',
          'numpy',
          'pyDOE2',
          'SALib',
          'matplotlib',
          'seaborn',
          'scipy',
          'future',
          'jpype1',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Science/Research',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)
