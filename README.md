# Listify – FastAPI + SQLite

Uma **API RESTful de gerenciamento de tarefas** construída com **FastAPI**, **SQLAlchemy** e **Pydantic**, com autenticação JWT, RBAC (Role-Based Access Control) e boas práticas de desenvolvimento.

---

## 🧩 Tecnologias Utilizadas

- **[FastAPI](https://fastapi.tiangolo.com/)** – Framework moderno, rápido e com documentação automática OpenAPI.
- **[SQLAlchemy](https://www.sqlalchemy.org/)** – ORM para mapear modelos Python para tabelas do SQLite.
- **[Pydantic](https://pydantic-docs.helpmanual.io/)** – Validação e serialização de dados de entrada e saída.
- **[Passlib](https://passlib.readthedocs.io/)** – Hash de senhas via bcrypt.
- **[JWT](https://jwt.io/)** – Autenticação baseada em token.
- **SQLite** – Banco de dados leve para persistência local, ideal para projetos pessoais e protótipos.

---

## 🏗 Arquitetura

- **Routers separados**:
  - `/auth` – criação de usuário, login e geração de token.
  - `/user` – informações do usuário e alteração de senha.
  - `/Tasks` – CRUD de tarefas do usuário autenticado.
  - `/admin` – operações administrativas (listar/excluir tasks de todos os usuários).
- **Models ORM**:
  - `UsersModel` – Usuários, com relacionamento `One-to-Many` para tarefas.
  - `ToDosModel` – Tarefas, cada uma pertencente a um usuário (`owner_id`).
- **Dependências FastAPI**:
  - `Depends(getDb)` – injeta sessão do SQLAlchemy.
  - `Depends(jwtEncryption.getCurrentUser)` – injeta usuário autenticado.
- **Segurança**:
  - Senhas armazenadas com bcrypt.
  - JWT com payload `{sub: username, id: user_id, role: user_role}`.
  - RBAC simples (`user` vs `admin`).

---

## 🛠 Funcionalidades

1. **Autenticação e Autorização**
   - Criação de usuários (`POST /auth`)
   - Login com JWT (`POST /auth/token`)
   - Proteção de rotas privadas
   - Diferenciação de permissões (`user` vs `admin`)

2. **CRUD de Tarefas**
   - Criar tarefa (`POST /Tasks`)
   - Listar tarefas do usuário (`GET /Tasks`)
   - Ler tarefa específica (`GET /Tasks/{task_id}`)
   - Atualizar tarefa (`PUT /Tasks/{task_id}`)
   - Excluir tarefa (`DELETE /Tasks/{task_id}`)

3. **Admin**
   - Listar todas tarefas (`GET /admin/todo`)
   - Excluir tarefas de qualquer usuário (`DELETE /admin/todo/{todo_id}`)

4. **Usuário**
   - Consultar dados do usuário (`GET /user`)
   - Alterar senha (`PUT /user/password`)

---

## 💻 Instalação e Execução

1. **Clone o repositório**  
```bash
git clone https://github.com/seu-usuario/todo-api.git
cd todo-api
````

2. **Crie um ambiente virtual**

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. **Instale dependências**

```bash
pip install -r requirements.txt
```

4. **Execute a API**

```bash
uvicorn main:app --reload
```

5. **Documentação automática**

* Swagger UI: `http://127.0.0.1:8000/docs`
* Redoc: `http://127.0.0.1:8000/redoc`

---

## 📂 Estrutura de Pastas

```
.
├─ Database/
│  ├─ database.py
│  └─ Models/
│     ├─ UsersModel.py
│     └─ ToDosModel.py
├─ Interfaces/
│  ├─ UserInterface.py
│  ├─ TaskInterface.py
│  ├─ TokenInterface.py
│  └─ UserPasswordVerificationInterface.py
├─ routers/
│  ├─ auth.py
│  ├─ users.py
│  ├─ toDos.py
│  └─ admin.py
├─ Utils/
│  └─ encryption.py
├─ main.py
└─ requirements.txt
```

---

## ⚡ Boas práticas aplicadas

* Injeção de dependências (`Depends`)
* Tipagem com `Annotated` e Pydantic
* Separação clara de responsabilidades (routers, models, utils)
* Uso de JWT e RBAC
* Respostas codificadas com `jsonable_encoder` para evitar recursão

---

## 🤔 Próximos passos

* ~~Implementar **Alembic** para versionamento de banco.~~
* Adicionar **testes automatizados** com Pytest.
* Suporte a refresh tokens.
* Suporte a bancos de dados maiores (PostgreSQL, MySQL).

---

## 📝 Contribuição

Pull requests são bem-vindos!
Sugestões de melhoria, refatorações ou testes adicionais são muito bem-vindas.

