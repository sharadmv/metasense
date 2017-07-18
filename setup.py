from setuptools import setup, find_packages

setup(name='metasense',
      version='1.0',
      packages=find_packages('.'),
      scripts=[
          "la/scripts/epa_join",
          "la/scripts/train_model",
          "la/scripts/test_model",
          "la/scripts/plot_axes",
          "la/scripts/get_epa_data"
      ]
     )
