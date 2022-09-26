import boto3
import json


def get_all_iam_users_policy():
    # Need Credential
    iam = boto3.client('iam')

    users = iam.list_users()
    user_names = [user['UserName'] for user in users['Users']]

    rows = []
    for user_name in user_names:
        result = iam.list_attached_user_policies(UserName=user_name)
        policies = result['AttachedPolicies']
        for policy in policies:
            policy_arn = policy['PolicyArn']
            managed = False
            policy_version = None
            policy_data = None

            if policy_arn.startswith('arn:aws:iam::aws:policy/'):
                managed = True
            if managed is False:
                policy_versions = iam.list_policy_versions(PolicyArn=policy_arn)
                policy_version = list(filter(lambda x: x['IsDefaultVersion'] is True, policy_versions['Versions']))[0][
                    'VersionId']
                policy_data = json.dumps(
                    iam.get_policy_version(PolicyArn=policy_arn, VersionId=policy_version)['PolicyVersion']['Document'],
                    indent=2)

            row = {}
            row['UserName'] = user_name
            row['PolicyName'] = policy['PolicyName']
            row['IsManagedPolicy'] = managed
            row['Inline'] = False
            row['Document'] = policy_data
            row['PolicyArn'] = policy_arn
            rows.append(row)

    inline_policy_rows = []
    for user_name in user_names:
        result = iam.list_user_policies(UserName=user_name)
        policy_names = result['PolicyNames']
        for policy_name in policy_names:
            policy = iam.get_user_policy(UserName=user_name, PolicyName=policy_name)
            policy_data = json.dumps(policy['PolicyDocument'], indent=2)
            row = {}
            row['UserName'] = user_name
            row['PolicyName'] = policy_name
            row['IsManagedPolicy'] = False
            row['Inline'] = True
            row['Document'] = policy_data
            inline_policy_rows.append(row)

    total_rows = []
    total_rows.extend(rows)
    total_rows.extend(inline_policy_rows)

    sorted_total_rows = list(sorted(total_rows, key=lambda x: x['UserName']))
    return sorted_total_rows


if __name__ == '__main__':
    rows = get_all_iam_users_policy()
    print(rows)

    # do something :)


