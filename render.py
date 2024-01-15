from jinja2 import Environment, FileSystemLoader
import os


from cluster_info import ClusterInfo


def generate_html_page(clusters: list[ClusterInfo], template_file, output_file):
    file_loader = FileSystemLoader(".")  # Load template from current directory
    env = Environment(loader=file_loader)
    template = env.get_template(template_file)

    html_output = template.render(clusters=clusters)

    with open(output_file, "w") as f:
        f.write(html_output)
