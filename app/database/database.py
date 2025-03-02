import boto3
from dotenv import load_dotenv

load_dotenv()

dynamodb = boto3.resource("dynamodb", region_name="us-east-1")

task_table = dynamodb.Table("ToDoList")
user_table = dynamodb.Table("Users")

def get_task_table():
    return task_table

def get_user_table():
    return user_table
