import os
import boto3
from dotenv import load_dotenv

# Carregar variáveis de ambiente do .env
load_dotenv()

# Configurar a conexão com o DynamoDB
dynamodb = boto3.resource("dynamodb",
    region_name=os.getenv("AWS_REGION", "us-east-1"),  # Pega do ambiente, padrão us-east-1
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),  # Pega do ambiente
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),  # Pega do ambiente
)

# Referência para as tabelas
task_table = dynamodb.Table("ToDoList")  # Tabela de tarefas
user_table = dynamodb.Table("Users")  # Tabela de usuários

# Dependência para obter referência das tabelas no FastAPI
def get_task_table():
    return task_table

def get_user_table():
    return user_table
