import os
import argparse
from bookmark_manager import BookmarkManager


def run_crawler(args):
    print(f"Import bookmarks from {args.bookmark_file}")
    from crawler import Crawler

    manager = BookmarkManager()
    cralwer = Crawler(manager)
    cralwer.parse(args.bookmark_file)
    cralwer.retrieve()
    manager.export(args.csv_file, lambda x: x.title != "" and x.description != "")


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
    from embedder import Embedder

    manager = BookmarkManager()
    manager.load(args.csv_file)
    manager.load_embedding(args.embedding_path)

    embedder = Embedder()
    cluster = ClusterManager(manager, embedder)
    cluster.cluster()
    manager.export(args.csv_file)
    manager.export_clusters(args.cluster_path)
    cluster.show()


def run_lda(args):
    print(f"Cluster bookmarks from {args.csv_file}")

    from lda import LDACluster

    manager = BookmarkManager()
    manager.load(args.csv_file)
    manager.load_embedding(args.embedding_path)

    cluster = LDACluster(manager)
    cluster.fit()
    labels = cluster.cluster()
    clusters = cluster.get_cluster_sentences()
    for i, cluster in clusters.items():
        print(cluster)
        print()
        # print(f"Cluster {k}, {labels[k]}")
        # for v in v[:10]:
        #     print("\t", v)


def run_visualizer(args):
    print("Running visualizer")
    from visualizer import Visualizer

    manager = BookmarkManager()
    manager.load(args.csv_file)
    manager.load_embedding(args.embedding_path)
    manager.load_clusters(args.cluster_path)

    visualizer = Visualizer(manager)
    visualizer.visualize()


def run_select_clusters(args):
    print("Running select clusters")
    manager = BookmarkManager()
    manager.load(args.csv_file)
    manager.export(args.save_file, lambda x: x.cluster in args.clusters)


def run_export(args):
    print("Running render")
    from render import generate_html_page

    manager = BookmarkManager()
    manager.load(args.csv_file)
    manager.load_clusters(args.cluster_path)

    generate_html_page(
        manager.clusters, template_file=args.template_file, output_file=args.output_file
    )


def run_all(args):
    run_crawler(args)
    run_embedder(args)
    run_cluster(args)
    run_visualizer(args)


def parse_args():
    parser = argparse.ArgumentParser(description="Process and visualize bookmark data.")
    parser.add_argument(
        "-d", "--dir", type=str, help="Path to the bookmark directory.", default="data"
    )

    parser.add_argument(
        "-c",
        "--csv_file",
        type=str,
        help="Path to the CSV file for embeddings.",
    )
    parser.add_argument(
        "-e",
        "--embedding_path",
        type=str,
        help="Path to save embeddings.",
    )
    parser.add_argument(
        "--cluster_path",
        type=str,
        help="Path to save embeddings.",
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

    lda_parser = subcmd.add_parser("lda", help="Run the cluster.")
    lda_parser.set_defaults(func=run_lda)

    select_parser = subcmd.add_parser("select", help="Select clusters.")
    select_parser.add_argument("save_file", type=str, help="Path to the bookmark file.")
    select_parser.add_argument(
        "clusters", type=int, nargs="+", help="Clusters to select."
    )
    select_parser.set_defaults(func=run_select_clusters)

    visualizer_parser = subcmd.add_parser("visualize", help="Run the visualizer.")
    visualizer_parser.set_defaults(func=run_visualizer)

    render_parser = subcmd.add_parser("export", help="Render the clusters.")
    render_parser.add_argument("output_file", type=str, help="Path to the output file.")
    render_parser.add_argument(
        "--template_file",
        type=str,
        help="Path to the template file.",
        default="template/bookmarks.html",
    )
    render_parser.set_defaults(func=run_export)

    run_all_parser = subcmd.add_parser("run", help="Run all.")
    run_all_parser.add_argument(
        "bookmark_file", type=str, help="Path to the bookmark file."
    )
    run_all_parser.set_defaults(func=run_all)

    return parser


def main():
    parser = parse_args()
    args = parser.parse_args()
    directory = args.dir
    if not os.path.exists(directory):
        os.makedirs(directory)

    if not args.csv_file:
        args.csv_file = os.path.join(directory, "bookmarks.csv")

    if not args.embedding_path:
        args.embedding_path = os.path.join(directory, "embeddings.npy")

    if not args.cluster_path:
        args.cluster_path = os.path.join(directory, "clusters.csv")

    if hasattr(args, "func"):
        args.func(args)
    else:
        # showing help
        parser.print_help()


if __name__ == "__main__":
    main()
