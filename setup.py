from setuptools import setup

requires = ['pyramid',
            'pyramid_chameleon',
            'pyramid_jinja2',
            'waitress',
]

setup(name='app',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = main:app
      """,
)
