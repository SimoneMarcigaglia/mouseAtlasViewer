from setuptools import setup

setup(
    name='mouseAtlasViewer',
    version='1.0',
    description="A python package for interactive 3D visualisation of mouse brain regions annotated in the Allen atlas.",
    url='https://github.com/SimoneMarcigaglia/mouseAtlasViewer',
    author='Simone Marcigaglia',
    author_email='marcigaglia.simone@live.com',
    license='BSD 2-clause',
    packages=['mouseAtlasViewer'],
    install_requires=['imageio-ffmpeg>=0.4.7',
                      'numpy>=1.23.1',
                      'pandas>=1.4.4',
                      'pynrrd>=1.0.0',
                      'PyQt5>=5.15.7',
                      'pyvista>=0.36.1',
                      'pyvistaqt>=0.9.0',
                      'tqdm>=4.64.1',
                      'wget>=3.2',
                      ],
    package_data={
        'mouseAtlasViewer': [
            'structure_tree_safe_2017.csv'
        ]
    },
    classifiers=[
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
    ],
)
