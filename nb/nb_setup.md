Install extensions:
pip install jupyter_contrib_nbextensions
jupyter contrib nbextension install --user

Or one step for all:
conda install -c conda-forge jupyter_contrib_nbextensions

Enable(sample):
jupyter nbextension enable codefolding/main



Install extension configurator:
conda install -c conda-forge jupyter_nbextensions_configurator
or use pip:
pip install jupyter_nbextensions_configurator
jupyter nbextensions_configurator enable --user

Use:
http://localhost:8888/nbextensions

