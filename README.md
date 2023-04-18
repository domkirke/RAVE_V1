# RAVE-v1

## Installing RAVE

- Install the [`miniconda`](https://docs.conda.io/en/latest/miniconda.html) dependency manager (RECOMMANDED)
- Create a specific environment
```shell
conda create -n RAVE python=3.8
```
-  Activate the RAVE environement
```
conda activate RAVE
```
- clone the repository in the target repository (replace YOUR_TARGET_FOLDER by your target location)
```
cd ${YOUR_TARGET_FOLDER}
git clone https://github.com/domkirke/RAVE_V1.git
cd RAVE_V1
```
- install the needed dependencies
```
pip install -r requirements.txt
```

## Training a RAVE model
The simplest method to train a RAVE is to first generate the needed instructions by executing the `cli_helper.py` script.
To do this, type : 
```
python3 cli_helper.py
```
and enter the required information for your training (leave empty to set to default value). This will export a `.txt` file at the root of `RAVE_V1.txt` named after the training name, specifying all the instructions to train/export the model and its prior. 
- *training name* : name of your training (will define the name of the folder containing the model & tensorboard)
- *path to .wav file*: the directory containing your audio files.
- *pre-processed data* : to be able to train on your files, RAVE must pre-process them in a *lmdb* format. This folder will contain the pre-processed data. 
- *sampling rate* : sampling rate of the training
- *multiband number* : number of filters for the PQMF
- *training example duration* : number of samples taken by RAVE during training. **Do not act on the latent space rate!**
- *configuration* : configuration of the model. `small` is low-capacity, but works on small devices such as Raspberry Pi. `default` is the default configuration (recommanded). `large` is a high-capcity model that works better, but probably too heavy for real-time applications.
- *prior resolution* : capacity of the prior (higher leads to a bigger but more accurate prior)
- *reconstruction fidelity* : will influence the number of latent dimensions during export for nn~ (0.9 means a target reconstruction of 90%)
- *latency compensation*: set to `True` for a no-latency real-time use (*warning : the system will have a lower generation capacity*)
- *latent size* : set a fixed latent size during export (learnt from reconstruction fidelity if set blank)
- *regularization strength* : latent regularization factor (0.0 will provide a better reconstruction but dangerously low generalization ability ; >0.1 the latent representation will be smoother, but the reconstruction may be poorer.)


**Warning!** if you train on remote GPUs, the training script will stop if you disconnect. To prevent the training process to be killed with your terminal, use `screen` to detach the training process from the terminal: 
```
# create your screen
screen -S screen_name
# launch your processes 
python3 train_rave.py {...}
```
then, you can press Ctrl+A, then D, to detach the process from your terminal. Then, you will be able to disconnect from the server without killing the training process. You can recall the screen by typing
```
# if you don't remember the name of the process, type the instruction below to list your screens
screen -ls
# then, recall the screen from its name
screen -r screen_name
```
