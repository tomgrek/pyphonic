import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.readlines()

setuptools.setup(
  name='Pyphonic',
  package_dir={"": "src"},
  packages=setuptools.find_packages(where="src"),
  python_requires=">=3.6",
  author='Tom Grek',
  author_email="tom.grek@gmail.com",
  version="0.9.1",
  description="Make a VST using Python",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url='https://github.com/tomgrek/pyphonic',
  keywords=['VST', 'Audio', 'MIDI', 'Realtime', 'AI', 'Deep Learning'],
  install_requires=requirements,
  classifiers=[
    'License :: Free for non-commercial use',
    'Topic :: Artistic Software',
    'Topic :: Multimedia :: Sound/Audio',
    'Topic :: Multimedia :: Sound/Audio :: MIDI',
    'Topic :: Multimedia :: Sound/Audio :: Sound Synthesis',
    'Topic :: Scientific/Engineering :: Artificial Intelligence',
    'Programming Language :: Python :: 3'
  ],
)