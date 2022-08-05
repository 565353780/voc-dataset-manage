# VOC Dataset Manage

## Labeled Dataset

please use

```bash
labelImg
```

and save .xml files in the default folder, make sure it looks like

```bash
<your-dataset-folder>
 |----0.jpg
 |----0.xml
 |----1.jpg
 |----1.xml
 |----...
```

## Install

```bash
conda create -n voc python=3.8
conda activate voc
pip install numpy opencv-python tqdm
```

## Run

### Simple

```bash
conda activate voc
python auto_cut_and_merge.py
```

### Step by step

```bash
conda activate voc
python switch_image_format.py
python cut_voc.py
python merge_voc.py
python voc_to_yolo.py
```

## Enjoy it~

