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

### Embed

```bash
python main.py embed
```

### Cluster

```bash
python main.py cluster
```

### Visualize

```bash
python main.py visualize
```

### Export

```bash
python main.py export exported.html
```
