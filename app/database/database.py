import os
import boto3
from dotenv import load_dotenv

# Carregar variáveis de ambiente do .env
load_dotenv()

# Configurar a conexão com o DynamoDB
dynamodb = boto3.resource("dynamodb", region_name="us-east-1")

# Referência para as tabelas
task_table = dynamodb.Table("ToDoList")  # Tabela de tarefas
user_table = dynamodb.Table("Users")  # Tabela de usuários

# Dependência para obter referência das tabelas no FastAPI
def get_task_table():
    return task_table

def get_user_table():
    return user_table
