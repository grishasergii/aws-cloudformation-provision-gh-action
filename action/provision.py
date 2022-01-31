import os

import click

from action.deploy import deploy
from action.package import package


@click.command()
@click.option("--stack-name", help="Stack name", required=True)
@click.option("--path", help="Path to the folder with CFN templates to package", required=True)
@click.option("--main-template", help="Name of the main template file", required=True)
@click.option("--branch", help="Branch name", required=True)
@click.option("--artifacts-bucket", help="S3 bucket for artifacts", required=True)
@click.option("--cfn-bucket", help="S3 bucket for cfn templates", required=True)
def provision(stack_name, path, main_template, branch, artifacts_bucket, cfn_bucket):
    click.echo(f"{'='*15} Package {'='*15}")
    package(stack_name, path, main_template, branch, artifacts_bucket, cfn_bucket)

    click.echo(f"{'=' * 15} Deploy {'=' * 15}")
    stack_id = deploy(os.path.join(path, main_template), stack_name, branch)
    click.echo(f"::set-output name=stack_id::{stack_id}")


if __name__ == "__main__":
    provision(auto_envvar_prefix="INPUT")
