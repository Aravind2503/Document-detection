#installing python venv
echo installing python venv...
sudo apt install python3-venv;

#creating the virtual environment
echo creating virtual env...
cd python; #inside python directory
python3 -m venv doc-detect-env;

#activating virtual environment
source doc-detect-env/bin/activate;

#installing python dependencies
echo "installing python libraries..."
pip3 install -r requirements.txt;

#installing tesseract ocr
echo "installing tesseract-ocr..."
sudo apt-install tesseract-ocr;

#installing python-3tk
echo "installing python-3tk for GUI"
sudo apt-install python3-tk;

#deactivating virtual environment
deactivate;

#coming back to home directory
cd ..;

#making required directories
echo 'making the required directories...'
mkdir python/resources/preprocessing_output;
mkdir python/resources/ml;
mkdir python/resources/ml/buffer;

mkdir python/resources/ml/test;
mkdir python/resources/ml/train;

#making directories for aadhar
mkdir python/resources/ml/test/aadhar;
mkdir python/resources/ml/train/aadhar;

#making directories for pan
mkdir python/resources/ml/test/pan;
mkdir python/resources/ml/train/pan;

mkdir python/resources/ml/buffer/test;
mkdir python/resources/ml/buffer/train;
mkdir uploads;

mkdir python/model/model1/assets;


#installing all the node dependencies
echo 'installing all node dependencies...'
npm install;

echo 'installation complete :)'