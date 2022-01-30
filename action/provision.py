import click

from action.deploy import deploy
from action.package import package


@click.command()
@click.option("--stack-name", help="Stack name")
@click.option("--path", help="Path to the folder with CFN templates to package")
@click.option("--main-template", help="Name of the main template file")
@click.option("--branch", help="Branch name")
@click.option("--artifacts-bucket", help="S3 bucket for artifacts")
@click.option("--cfn-bucket", help="S3 bucket for cfn templates")
def provision(stack_name, path, main_template, branch, artifacts_bucket, cfn_bucket):
    if not artifacts_bucket or not cfn_bucket:
        raise ValueError("artifacts and cfn bucket names must be set")

    click.echo(f"{'='*15} Package {'='*15}")
    package(stack_name, path, main_template, branch, artifacts_bucket, cfn_bucket)

    click.echo(f"{'=' * 15} Deploy {'=' * 15}")
    stack_id = deploy(main_template, stack_name, branch)
    click.echo(f"::set-output name=time::{stack_id}")


if __name__ == "__main__":
    provision(auto_envvar_prefix="INPUT")
