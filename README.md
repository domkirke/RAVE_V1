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
python3 cli_helper.txt
```
and enter the required information for your training (leave empty to set to default value). This will export a `.txt` file at the root of `RAVE_V1.txt` named after the training name, specifying all the instructions to train/export the model and its prior.

