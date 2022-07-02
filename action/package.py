import os
import shutil
from pathlib import Path

import click

from action.external_cmd import ExternalCmd


def package(stack_name, path, main_template, branch, environment, artifacts_bucket, cfn_bucket):
    out_dir = os.path.join("build", "templates")
    if Path(out_dir).exists():
        shutil.rmtree(out_dir)
    Path(out_dir).mkdir(exist_ok=True, parents=True)

    for template_file in os.listdir(path):
        if template_file.endswith(".cfn"):
            if template_file == main_template:
                continue
            template_file_full_path = os.path.join(path, template_file)
            out_path = os.path.join(out_dir, template_file)
            click.echo(f"Packaging {template_file} to {out_path}")
            ExternalCmd.run(
                f"aws cloudformation package "
                f"--template-file {template_file_full_path} "
                f"--s3-bucket {artifacts_bucket} "
                f"--s3-prefix {stack_name}/{environment}/{branch} "
                f"--output-template-file {out_path}"
            )

            click.echo(f"Uploading {out_path} to {cfn_bucket}")
            ExternalCmd.run(
                f"aws s3 cp {out_path} s3://{cfn_bucket}/{stack_name}/{environment}/{branch}/{template_file}"
            )
