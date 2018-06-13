# ComputerScientistColoringBook
A neural network-oriented project about coloring vintage black and white cartoons, without going out of the lines.

## Prerequisites

We require you to have Anaconda installed on your computer.

## How to set up the environment

For now we encourage you to use Anaconda package manager and creation of the environments.
In order to create an environment you have to run the following command providing the environment name:

```
conda env create -n <your_environment_name> -f <enviroment_file_name>
```

To activate the environment you have to run the following command:

```
activate <your_environment_name>
```

After running this command you will see something like this:

```
(<name_of_environment) C:\Windows\system32>
```

To deactivate environment run:

```
deactivate
```

## How to make side by side movie
To prepare side-by-side movie first we have to make a folder in merge_images directory with a name of a movie. Inside this folder two folders are required. First called 'bw' and second called 'colored'. In the first one place black and white images and colored in the second one. Please remember that images must be names as a integer number representing the frame number (based on this these two images will be merged). Valid file names is for example '0.png' or '1223.png'.

Having this part done you can run the following command:
```
python merge_images.py
```
Running this command in every movie folder will place an extra folder called 'merged_<name_of_a_movie>' in which there will be side-by-side consecutive frames.

## How to make a movie from images
In order to make a movie from images you have to fun the following command
```
python movie_preparation.py <path_to_folder>
```
Running this command can take monger amount of time for a large set of images (1000 images takes around 5 seconds 16GB RAM i7-4700k).