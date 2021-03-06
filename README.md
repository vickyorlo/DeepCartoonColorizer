# DeepCartoonColorizer
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

## Running our code
Our main file consists of several options.

### Creating frames from movies
The command below will take folder with movies specified by <movies_folder_name> and prepare a folder called 'training_frames' in which there will be folder named after every cartoon with consecutive frames inside.
```
python main.py -i <movies_folder_name>
```
This will look like this.
```
├───training_frames
│   └───Teraz Miki! - Cenne zapasy.mp4
```

### Preparing testing and training set
Once frames creation is done the training and testing set can be extracted using the command below.
```
python main.py -et
```
You can also set -s (stride) option for example:
```
python main.py -et -s 100 # means that every 100 frame will considered
```
By default it is 50 (around 2 seconds as in publication).

Running one of this commands will result in creation of two folders. One called 'training_set' and second 'testing_set'.

The split will use images only from 'training_frames' folder.
### Model training ###

To train the model the training_set folder is needed with the training images inside.
Having that please enter command below.
```
python main.py -t
```
There is also possibility to set:
* number of epochs with -e option (1000 default),
* batch size with -b option (5 default).

Example command:
```
python main.py -t -e 10 -b 3
```
Successful run of this command will produce you the model file `model_1e_pic_m.h5` and logs file `events.out.tfevents.1532362895` placed in `/logs` directory.

In the folder called 'trained_models' there is a trained model that was used in publication. The model is called `model_1000e_pic_m.h5`
### Color directory having pre-trained model

To color images having trained model the following command is needed:
```
python main.py -c -m <model_file>
```

The command will take every movie folder from 'testing_set' and color it using model provided.

There is also option to specify your own testing folder with -o option. 
```
python main.py -c -m <model_file> -o <folder_name>
```
**Please remember that the directory you provide need to have an extra folder inside with images you want to color in it for example:**
```
└───your_folder
    ├───movie1
    │       example_name.png
    │
    └───movie2
            example_name.png
```

### Run all stages ###
There is also possibility to run all of the previous stages using one command:
```
python main.py -a -i <folder_name_with_movies>
```
Also -e and -b arguments can be specified. Without them the code will run as presented in publication.

## How to make side by side movie
To prepare side-by-side movie first we have to make a folder in merge_images directory with a name of a movie. Inside this folder two folders are required. First called 'bw' and second called 'colored'. In the first one place black and white images and colored in the second one. Please remember that images must be names as an integers representing the frame number (based on this, these two images will be merged). Valid file names is for example '0.png' or '1223.png'.

The merged_images directory should look like this:
```
├───movie1
│   ├───bw
│   └───colored
└───movie2
    ├───bw
    └───colored
```

Having this part done you can run the following command:
```
python merge_images.py
```
Running this command in every movie folder will place an extra folder called 'merged_<name_of_a_movie>' in which there will be side-by-side consecutive frames.

## How to make a movie from images
In order to make a movie from images you have to run the following command
```
python movie_preparation.py <path_to_folder>
```
Running this command will take greater amount of time for a large set of images (1000 images take around 5 seconds 16GB RAM i7-4700k).

## Citation

The source code of the Deep Cartoon Colorizer may be used for non-commercial research provided you acknowledge the source by citing the following paper:
* Mariusz Chybicki, Wiktor Kozakiewicz, Dawid Sielski, Anna Fabijańska: Deep cartoon colorizer: An automatic approach for colorization of vintage cartoons, Engineering Applications of Artificial Intelligence, vol. 81, 2019, pp. 37-46, doi: 10.1016/j.engappai.2019.02.006 [Link](https://doi.org/10.1016/j.engappai.2019.02.006), [BibTEX](https://github.com/vickyorlo/DeepCartoonColorizer/blob/master/DCC.BIB)

```
@article{Chybicki2019,
	author 	= {Mariusz Chybicki and Wiktor Kozakiewicz and Dawid Sielski and Anna Fabija\'{n}ska},
	title	= {Deep cartoon colorizer: An automatic approach for colorization of vintage cartoons},
	journal = {Engineering Applications of Artificial Intelligence},
	volume	= {81},
	pages 	= {37--46},
	year 	= {2019},
	issn 	= {0952-1976},
	doi 	= {https://doi.org/10.1016/j.engappai.2019.02.006},
	url 	= {http://www.sciencedirect.com/science/article/pii/S0952197619300296}
}
```

## Authors

* **Mariusz Chybicki** - [mariusz.chybicki@gmail.com](mariusz.chybicki@gmail.com)
* **Wiktor Kozakiewicz** - [wikkozakiewicz@gmail.com](wikkozakiewicz@gmail.com)
* **Dawid Sielski** - [dawid.sielski@outlook.com](dawid.sielski@outlook.com)
* **Anna Fabijańska** - [anna.fabijanska@p.lodz.pl](anna.fabijanska@p.lodz.pl)
