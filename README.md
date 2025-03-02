# To-Do List API

Projeto de TCC utilizando FastAPI e Angular.

## Descrição

Este projeto é uma aplicação de lista de tarefas (To-Do List) desenvolvida como parte do Trabalho de Conclusão de Curso (TCC) em Desenvolvimento Web Full Stack. A aplicação é composta por um backend desenvolvido em FastAPI e um frontend desenvolvido em Angular. A aplicação permite que os usuários registrem, façam login e gerenciem suas tarefas.

## Tecnologias Utilizadas

- **Backend**: FastAPI
- **Frontend**: Angular
- **Banco de Dados**: DynamoDB (simulado com `moto` para testes)
- **Autenticação**: JWT (JSON Web Tokens)
- **Testes**: Pytest, Unittest, Moto

## Funcionalidades

- Registro de Usuário
- Login de Usuário
- Criação de Tarefas
- Listagem de Tarefas
- Atualização de Tarefas
- Exclusão de Tarefas
- Autenticação e Autorização com JWT

## Requisitos

- Python 3.8+
- Node.js 14+
- AWS CLI (para configuração do DynamoDB)

## Instalação

### Backend

1. Clone o repositório:
   ```bash
   git clone https://github.com/EricDamasc/todo-list-backend.git
   cd todo-list-backend
   ```

2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows use `venv\Scripts\activate`
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure as variáveis de ambiente: Crie um arquivo `.env` na raiz do projeto e adicione as seguintes variáveis:
   ```
   SECRET_KEY=your_secret_key
   AWS_REGION=us-east-1
   ```

5. Execute a aplicação:
   ```bash
   uvicorn app.main:app --reload
   ```

### Frontend

1. Clone o repositório do frontend:
   ```bash
   git clone https://github.com/EricDamasc/todo-list-frontend.git
   cd todo-list-frontend
   ```

2. Instale as dependências:
   ```bash
   npm install
   ```

3. Execute a aplicação:
   ```bash
   ng serve
   ```

## Testes

### Backend

Para rodar os testes do backend, utilize o comando:
```bash
pytest
```
Os testes utilizam a biblioteca `moto` para simular o DynamoDB e `unittest.mock` para mockar as funções de autenticação e interação com o banco de dados.

### Frontend

Para rodar os testes do frontend, utilize o comando:
```bash
ng test
```

## Estrutura do Projeto

### Backend

```
todo-list-backend/
├── app/
│   ├── api/
│   │   ├── endpoints/
│   │   └── dependencies.py
│   ├── core/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── main.py
│   └── ...
├── tests/
│   ├── test_api/
│   ├── test_services/
│   └── ...
├── .env
├── requirements.txt
└── ...
```

### Frontend

```
todo-list-frontend/
├── src/
│   ├── app/
│   │   ├── components/
│   │   ├── services/
│   │   ├── models/
│   │   ├── app.module.ts
│   │   └── ...
├── angular.json
├── package.json
└── ...
```

## Endpoints da API

### Autenticação

- **POST /register**: Registra um novo usuário.
  - Request Body: `{"email": "string", "password": "string", "username": "string"}`
  - Response: `{"access_token": "string", "token_type": "bearer"}`

- **POST /login**: Faz login de um usuário.
  - Request Body: `{"email": "string", "password": "string"}`
  - Response: `{"access_token": "string", "token_type": "bearer"}`

### Tarefas

- **GET /tasks**: Retorna todas as tarefas do usuário autenticado.
  - Response: `[{"task_id": "string", "title": "string", "description": "string", "completed": "boolean", "due_date": "string", "priority": "string"}]`

- **POST /tasks**: Cria uma nova tarefa.
  - Request Body: `{"title": "string", "description": "string", "completed": "boolean", "due_date": "string", "priority": "string"}`
  - Response: `{"task_id": "string", "title": "string", "description": "string", "completed": "boolean", "due_date": "string", "priority": "string"}`

- **PUT /tasks/{task_id}**: Atualiza uma tarefa existente.
  - Request Body: `{"title": "string", "description": "string", "completed": "boolean", "due_date": "string", "priority": "string"}`
  - Response: `{"task_id": "string", "title": "string", "description": "string", "completed": "boolean", "due_date": "string", "priority": "string"}`

- **DELETE /tasks/{task_id}**: Deleta uma tarefa existente.
  - Response: `{"message": "Tarefa removida com sucesso"}`

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma issue ou enviar um pull request.
