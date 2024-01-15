import argparse
from bookmark_manager import BookmarkManager


def run_crawler(args):
    print(f"Import bookmarks from {args.bookmark_file}")
    from crawler import Crawler

    manager = BookmarkManager()
    cralwer = Crawler(manager)
    cralwer.parse(args.bookmark_file)
    cralwer.retrieve()
    manager.export(args.csv_file)


def run_embedder(args):
    print(f"Embed bookmarks from {args.csv_file} to {args.embedding_path}")
    from embedder import Embedder
    import numpy as np

    manager = BookmarkManager()
    manager.load(args.csv_file)
    embedder = Embedder()
    embbedings = embedder.embed(manager.get_sentences())
    np.save(args.embedding_path, embbedings)


def run_cluster(args):
    print(f"Cluster bookmarks from {args.csv_file}")

    from cluster import ClusterManager

    manager = BookmarkManager()
    manager.load(args.csv_file)
    manager.load_embedding(args.embedding_path)

    cluster = ClusterManager(manager)
    cluster.cluster()
    manager.export(args.csv_file)
    manager.export_clusters(args.cluster_path)
    cluster.show()


def run_labeler(args):
    print("Running labeler")
    from cluster_labeler import ClusterLabeler

    manager = BookmarkManager()
    manager.load(args.csv_file)
    manager.load_embedding(args.embedding_path)
    manager.load_clusters(args.cluster_path)

    labeler = ClusterLabeler()
    for cluster in manager.clusters:
        label = labeler.label(cluster)
        print(cluster)
    manager.export_clusters(args.cluster_path)


def run_visualizer(args):
    print("Running visualizer")
    from visualizer import Visualizer

    manager = BookmarkManager()
    manager.load(args.csv_file)
    manager.load_embedding(args.embedding_path)
    manager.load_clusters(args.cluster_path)

    visualizer = Visualizer(manager)
    visualizer.visualize()


def run_all(args):
    run_crawler(args)
    run_embedder(args)
    run_cluster(args)
    run_labeler(args)
    run_visualizer(args)


def parse_args():
    parser = argparse.ArgumentParser(description="Process and visualize bookmark data.")
    parser.add_argument(
        "-c",
        "--csv_file",
        type=str,
        help="Path to the CSV file for embeddings.",
        default="data/bookmarks.csv",
    )
    parser.add_argument(
        "-e",
        "--embedding_path",
        type=str,
        help="Path to save embeddings.",
        default="data/embeddings.npy",
    )
    parser.add_argument(
        "--cluster_path",
        type=str,
        help="Path to save embeddings.",
        default="data/clusters.csv",
    )

    subcmd = parser.add_subparsers(
        dest="subcmd", help="Action to perform.", metavar="cmd"
    )

    crawler_parser = subcmd.add_parser(
        "crawl", help="Import bookmarks and retrieve data."
    )
    crawler_parser.add_argument(
        "bookmark_file", type=str, help="Path to the bookmark file."
    )
    crawler_parser.set_defaults(func=run_crawler)

    embedder_parser = subcmd.add_parser("embed", help="Run the embedder.")
    embedder_parser.set_defaults(func=run_embedder)

    cluster_parser = subcmd.add_parser("cluster", help="Run the cluster.")
    cluster_parser.set_defaults(func=run_cluster)

    labeler_parser = subcmd.add_parser("label", help="Run the labeler.")
    labeler_parser.set_defaults(func=run_labeler)

    visualizer_parser = subcmd.add_parser("visualize", help="Run the visualizer.")
    visualizer_parser.set_defaults(func=run_visualizer)

    run_all_parser = subcmd.add_parser("run", help="Run all.")
    run_all_parser.add_argument(
        "bookmark_file", type=str, help="Path to the bookmark file."
    )
    run_all_parser.set_defaults(func=run_all)

    return parser


def main():
    parser = parse_args()
    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        # showing help
        parser.print_help()


if __name__ == "__main__":
    main()
