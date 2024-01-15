import argparse


def run_all(args):
    print("Running all")


def run_crawler(args):
    print("Running crawler")


def run_embedder(args):
    print("Running embedder")


def run_cluster(args):
    print("Running cluster")


def run_visualizer(args):
    print("Running visualizer")


def parse_args():
    parser = argparse.ArgumentParser(description="Process and visualize bookmark data.")
    parser.add_argument(
        "-b", "--bookmark_file", type=str, help="Path to the bookmark file."
    )
    parser.add_argument(
        "-c", "--csv_file", type=str, help="Path to the CSV file for embeddings."
    )
    parser.add_argument(
        "-e", "--embedding_path", type=str, help="Path to save embeddings."
    )

    subcmd = parser.add_subparsers(
        dest="subcmd", help="Action to perform.", metavar="cmd"
    )

    crawler_parser = subcmd.add_parser(
        "crawl", help="Import bookmarks and retrieve data."
    )
    crawler_parser.set_defaults(func=run_crawler)

    embedder_parser = subcmd.add_parser("embed", help="Run the embedder.")
    embedder_parser.set_defaults(func=run_embedder)

    cluster_parser = subcmd.add_parser("cluster", help="Run the cluster.")
    cluster_parser.set_defaults(func=run_cluster)

    visualizer_parser = subcmd.add_parser("visualize", help="Run the visualizer.")
    visualizer_parser.set_defaults(func=run_visualizer)

    return parser.parse_args()


def main():
    args = parse_args()
    if hasattr(args, "func"):
        args.func(args)


if __name__ == "__main__":
    main()
