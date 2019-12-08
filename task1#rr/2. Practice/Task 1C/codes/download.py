import wget


url='https://drive.google.com/uc?export=download&confirm=Uq6r&id=1Akn4mrJDA3YeIup0r2MKa0eh06yx_RdO'
print("downloading....")
wget.download(url)
print("download complete")