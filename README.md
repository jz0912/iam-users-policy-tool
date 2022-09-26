# iam-users-role-tool

### Usage
  - AWS IAM 상에 등록된 IAM-User 에게 붙어있는 Role 정보를 알 수 있는 도구

### Description
  - boto3 를 사용하여 IAM API 호출, Credential 세팅 필요

### Output
  - UserName: IAM User 의 UserName
  - PolicyName: User 에게 붙어있는 정책 이름
  - IsManagedPolicy (True/False): 붙어있는 Policy 의 AWS Managed Policy 여부 (ex: AmazonS3ReadOnlyAccess)
  - Inline (True/False): 해당 정책이 인라인 정책인지의 여부
  - Document: 해당 정책의 json (Managed Policy 인 경우, 빈칸)
  - PolicyArn: 해당 정책의 ARN (Inline 정책인 경우, 빈칸)
