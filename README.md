# AI Bookmark Manager

## Installation

```bash
pip install -r requirements.txt
```

## Usage

    python main.py [options]

```bash
usage: main.py [-h] [-d DIR] [-c CSV_FILE] [-e EMBEDDING_PATH] [--cluster_path CLUSTER_PATH] cmd ...

Process and visualize bookmark data.

positional arguments:
  cmd                   Action to perform.
    crawl               Import bookmarks and retrieve data.
    embed               Run the embedder.
    cluster             Run the cluster.
    lda                 Run the cluster.
    select              Select clusters.
    visualize           Run the visualizer.
    render              Render the clusters.
    run                 Run all.

options:
  -h, --help            show this help message and exit
  -d DIR, --dir DIR     Path to the bookmark directory.
  -c CSV_FILE, --csv_file CSV_FILE
                        Path to the CSV file for embeddings.
  -e EMBEDDING_PATH, --embedding_path EMBEDDING_PATH
                        Path to save embeddings.
  --cluster_path CLUSTER_PATH
                        Path to save embeddings.
```

### Crawl

```bash
python main.py crawl bookmarks_import.html
```

This command will import the bookmarks from the `bookmarks_import.html` file and retrieve the metadata for each bookmark. The data will be saved in the `data` folder. This command may take a while to complete.

You can use `raw_data/bookmarks_12_30_23.html` as a sample file.

    python main.py crawl raw_data/bookmarks_12_30_23.html

### Embed

This command will convert the data saved in the CSV file into embeddings. The embeddings will be saved to `data/embeddings.npy`.

```bash
python main.py embed
```

### Cluster

This command will cluster the bookmarks and select title for each cluster. The clusters metadata will be saved to `data/clusters.json`, and write back the cluster label to each bookmarks.

```bash
python main.py cluster
```

### Visualize

This command will visualize the clusters as a interactive Matplotlib figure. You can hover on the points to see the title of the bookmarks.

```bash
python main.py visualize
```

### Export

This command will export the clusters as a HTML file. This file can be imported into your browser as a bookmark file.

    python main.py export exported.html

This command will export the clusters as a easy-to-read HTML file. It cannot be imported but you can open the HTML file in your browser to see the clusters and bookmarks. This file also displays the clustering score for each cluster.

    python main.py export show.html --template_file template/show.html

## Run Sample Data

We have prepared a set of data for you to run in the `cleaned_data` folder. You can run the following command to run the whole pipeline.

    python main.py -d cleaned_data embed
    python main.py -d cleaned_data cluster
    python main.py -d cleaned_data visualize
    python main.py -d cleaned_data export output.html
