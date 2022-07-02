import click

from action.external_cmd import ExternalCmd


def _stack_exists(stack_name):
    result = ExternalCmd.run_and_parse_json(
        f"aws cloudformation list-stacks --stack-status-filter "
        "UPDATE_COMPLETE "
        "CREATE_COMPLETE "
        "UPDATE_IN_PROGRESS "
        "UPDATE_COMPLETE_CLEANUP_IN_PROGRESS "
        "ROLLBACK_COMPLETE "
        "UPDATE_ROLLBACK_COMPLETE "
    )
    stacks = result.get("StackSummaries", [])
    for stack in stacks:
        if stack["StackName"] == stack_name:
            return True
    return False


def deploy(template_file, stack_name, branch, environment, cfn_bucket_name, aws_region):
    stack_name = f"{stack_name}-{branch}-{environment}"
    click.echo(f"Provisioning {stack_name}")
    cf_bucket_url = f"https://{cfn_bucket_name}.s3.{aws_region}.amazonaws.com"
    if _stack_exists(stack_name):
        click.echo(f"Stack '{stack_name}' already exists. Will update")
        result = ExternalCmd.run_and_parse_json(
            f"aws cloudformation update-stack "
            f"--stack-name {stack_name} "
            f"--template-body file://{template_file} "
            f"--parameters ParameterKey=Branch,ParameterValue={branch} "
            f"--parameters ParameterKey=Environment,ParameterValue={environment} "
            f"ParameterKey=CfnBucketUrl,ParameterValue={cf_bucket_url} "
            "--tags file://tags.json "
            "--capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM CAPABILITY_AUTO_EXPAND"
        )
        stack_id = result["StackId"]
        click.echo("Waiting for the stack-update-complete confirmation...")
        ExternalCmd.run(
            f"aws cloudformation wait stack-update-complete --stack-name {stack_id}"
        )
    else:
        click.echo(f"Stack '{stack_name}' does not exist. Will create")
        result = ExternalCmd.run_and_parse_json(
            f"aws cloudformation create-stack "
            f"--stack-name {stack_name} "
            f"--template-body file://{template_file} "
            f"--parameters ParameterKey=Branch,ParameterValue={branch} "
            f"ParameterKey=CfnBucketUrl,ParameterValue={cf_bucket_url} "
            "--tags file://tags.json "
            "--capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM CAPABILITY_AUTO_EXPAND"
        )
        stack_id = result["StackId"]
        click.echo("Waiting for the stack-create-complete confirmation...")
        ExternalCmd.run(
            f"aws cloudformation wait stack-create-complete --stack-name {stack_id}"
        )

    click.echo("Confirmed")
    return stack_id
