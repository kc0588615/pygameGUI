# Remove card-related packages and dependencies
setup(
    name="pygame-examples",
    packages=find_packages(),
    install_requires=[
        "pygame>=2.0.0",
        "pygame_gui>=0.6.0",  # Add pygame_gui as a dependency
        "numpy>=1.19.0",
        "opencv-python>=4.5.0",
    ],
) 