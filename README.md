# 🟠 Mastermind — Desafio Técnico Full-Stack Jr.

Um jogo Mastermind digital completo, com autenticação JWT, lógica de jogo no backend, tabuleiro interativo no frontend e ranking global.

---

## Sumário

- [Visão geral](#visão-geral)
- [Stack tecnológica](#stack-tecnológica)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Pré-requisitos](#pré-requisitos)
- [Rodando o backend](#rodando-o-backend)
- [Rodando o frontend](#rodando-o-frontend)
- [Variáveis de ambiente](#variáveis-de-ambiente)
- [Rodando os testes](#rodando-os-testes)
- [Documentação da API](#documentação-da-api)
- [Decisões técnicas](#decisões-técnicas)
- [Regras do jogo](#regras-do-jogo)
- [Prints das telas do jogo] (#prints-das-telas-do-projeto)

---

## Visão geral

Mastermind é um jogo de lógica onde o jogador tenta adivinhar uma sequência secreta de 4 cores (letras A–F) em até **10 tentativas**. A cada tentativa, o backend retorna quantas posições estão corretas e quantas cores certas estão na posição errada — sem revelar o código secreto.

O sistema possui:
- Cadastro e login com JWT
- Criação e validação de partidas no backend
- Tabuleiro visual responsivo com tema laranja
- Ranking global ordenado por melhor pontuação
- Histórico de partidas por usuário

---

## Stack tecnológica

| Camada        | Tecnologia                        |
|---------------|-----------------------------------|
| Backend       | Python 3.11+ · FastAPI · SQLAlchemy |
| Banco de dados | SQLite (relacional, zero config)  |
| Frontend      | Angular 20 · SCSS · Standalone Components |
| Autenticação  | JWT (PyJWT + passlib/bcrypt)      |
| API Docs      | Swagger/OpenAPI (embutido FastAPI) |
| Testes backend| pytest + httpx (TestClient)       |
| Testes frontend| Karma + Jasmine (Angular padrão) |

---

## Estrutura do projeto

```
mastermind/
├── backend/
│   ├── app/
│   │   ├── main.py              # Entrypoint FastAPI
│   │   ├── config.py            # Configurações via .env
│   │   ├── database.py          # Engine SQLAlchemy + sessão
│   │   ├── models.py            # Modelos ORM (User, Game)
│   │   ├── schemas.py           # Schemas Pydantic (request/response)
│   │   ├── security.py          # JWT + bcrypt
│   │   ├── exceptions.py        # Handlers globais de erro
│   │   ├── routers/             # Controllers HTTP
│   │   │   ├── auth_router.py
│   │   │   ├── game_router.py
│   │   │   ├── ranking_router.py
│   │   │   └── user_router.py
│   │   └── services/            # Lógica de negócio
│   │       ├── auth_service.py
│   │       └── game_service.py
│   ├── tests/
│   │   ├── conftest.py
│   │   ├── test_auth.py
│   │   ├── test_game.py
│   │   └── test_game_service.py
│   ├── requirements.txt
│   └── .env.example
│
└── frontend/
    └── src/
        └── app/
            ├── guards/           # AuthGuard + GuestGuard
            ├── interceptors/     # Bearer token interceptor
            ├── models/           # Interfaces TypeScript
            ├── pages/            # Login, Register, Dashboard, Game, Ranking
            └── services/         # AuthService, GameService, AuthStorageService
```

---

## Pré-requisitos

| Ferramenta         | Versão mínima |
|--------------------|---------------|
| Python             | 3.11          |
| pip                | 23+           |
| Node.js            | 18+           |
| npm                | 9+            |
| Angular CLI        | 17+           |
| Google Chrome      | qualquer (para testes frontend) |

---

## Rodando o backend

```bash
# 1. Entrar na pasta
cd backend

# 2. Criar e ativar o ambiente virtual
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Copiar o arquivo de variáveis de ambiente
cp .env.example .env
# Edite o .env e defina um SECRET_KEY seguro

# 5. Iniciar o servidor
uvicorn app.main:app --reload --port 8000
```

O banco SQLite (`mastermind.db`) é criado automaticamente na primeira execução.

---

## Rodando o frontend

```bash
# 1. Entrar na pasta
cd frontend

# 2. Instalar dependências
npm install

# 3. Iniciar o servidor de desenvolvimento
ng serve
```

Acesse http://localhost:4200

> O frontend se comunica com o backend em `http://localhost:8000` (configurável em `src/environments/environment.ts`).

---

## Variáveis de ambiente

Arquivo: `backend/.env` (copie de `.env.example`)

| Variável                      | Descrição                               | Exemplo                             |
|-------------------------------|------------------------------------------|--------------------------------------|
| `SECRET_KEY`                  | Chave secreta para assinar JWT           | `minha-chave-super-secreta-32chars` |
| `ALGORITHM`                   | Algoritmo JWT                            | `HS256`                              |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Expiração do token em minutos           | `60`                                 |
| `DATABASE_URL`                | String de conexão SQLAlchemy            | `sqlite:///./mastermind.db`          |
| `DEBUG_LOG_SECRETS`           | Exibe segredo do jogo nos logs (debug)  | `false`                              |


### Geração de `SECRET_KEY` segura

PowerShell (Windows):

```powershell
$rng = New-Object System.Security.Cryptography.RNGCryptoServiceProvider
$bytes = New-Object byte[] 48
$rng.GetBytes($bytes)
$rng.Dispose()
[Convert]::ToBase64String($bytes).Replace('+','-').Replace('/','_').TrimEnd('=')
```

Para os utilizadores:
- O repositório deve conter apenas o `backend/.env.example`.
- Cada pessoa que for rodar o projeto copia para `backend/.env` e define seu próprio `SECRET_KEY`.

---

## Rodando os testes

### Backend

```bash
cd backend
venv\Scripts\activate   # ou source venv/bin/activate
pytest tests/ -v
```

Resultado esperado: **19 testes passando**

### Frontend

```bash
cd frontend
ng test --watch=false --browsers=ChromeHeadless
```

Resultado esperado: **12 testes passando**

---

## Documentação da API

Com o backend rodando, acesse:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **OpenAPI JSON:** http://localhost:8000/openapi.json

### Endpoints principais

| Método | Rota                        | Descrição                         | Auth |
|--------|-----------------------------|-----------------------------------|------|
| POST   | `/auth/register`            | Criar conta                       | ❌   |
| POST   | `/auth/login`               | Login → retorna JWT               | ❌   |
| GET    | `/users/me`                 | Dados do usuário logado           | ✅   |
| POST   | `/games/start`              | Iniciar nova partida              | ✅   |
| POST   | `/games/{id}/attempt`       | Submeter tentativa                | ✅   |
| GET    | `/games/{id}`               | Estado da partida                 | ✅   |
| GET    | `/games/`                   | Histórico de partidas             | ✅   |
| GET    | `/ranking/`                 | Ranking global                    | ✅   |

---

## Decisões técnicas

### Backend
- **FastAPI**: Framework moderno, async-ready, com Swagger embutido, validação automática via Pydantic e ótima DX.
- **SQLAlchemy + SQLite**: Banco relacional com zero configuração para rodar localmente. A `DATABASE_URL` pode ser trocada para PostgreSQL/MySQL sem mudar código.
- **Arquitetura em camadas**: `Router → Service → Repository (SQLAlchemy ORM)` — lógica de negócio isolada nos Services, Controllers apenas recebem/retornam HTTP.
- **JWT com PyJWT + passlib/bcrypt**: Autenticação stateless. O código secreto do jogo é armazenado apenas no backend e **nunca** exposto ao frontend durante a partida.
- **Pontuação**: `(11 - tentativas) × 100` para vitórias. Derrota = 0 pontos.

### Frontend
- **Angular 20 Standalone**: Sem NgModules — componentes independentes, mais simples e alinhados com o futuro do Angular.
- **Lazy loading**: Cada página é carregada sob demanda via `loadComponent`.
- **Signals**: `signal()` e `computed()` para estado reativo sem `BehaviorSubject`.
- **HTTP Interceptor funcional**: Injeta automaticamente o header `Authorization: Bearer <token>` em todas as requisições.
- **Tema laranja**: Paleta definida em CSS custom properties (`:root`), aplicada globalmente.
- **Sem lógica de negócio nos templates**: Toda validação e lógica está nos componentes TypeScript e services.

---

## Regras do jogo

- O código secreto tem **4 posições**, cada uma com uma de 6 cores: `A B C D E F`
- O jogador tem **10 tentativas**
- A cada tentativa, o feedback mostra:
  - 🟠 **Posição correta** (cor certa, lugar certo)
  - ⬜ **Cor correta, posição errada**
- O código secreto é gerado no backend e **nunca enviado ao frontend** durante o jogo
- Ao acabar (vitória ou esgotamento), o código secreto é revelado e a pontuação calculada


---
## Prints das telas do Projeto
### Tela de login
<img width="1919" height="904" alt="image tela login" src="https://github.com/user-attachments/assets/081a5835-c423-4612-a421-a3941ac216f2" />

### Tela de Cadastro
<img width="1919" height="907" alt="image" src="https://github.com/user-attachments/assets/97af98f0-6ea4-4f16-ae30-b0d9d73d019c" />

### Tela inicial
<img width="1919" height="916" alt="image" src="https://github.com/user-attachments/assets/d695ba40-d25e-4428-8a34-7b3a28894afd" />

### Tela do jogo iniciado
<img width="1919" height="909" alt="image" src="https://github.com/user-attachments/assets/ce0ac365-f0ea-4ddd-9136-20123cac98a0" />

### Tela do Ranking Global
<img width="1919" height="906" alt="image" src="https://github.com/user-attachments/assets/2fa55c89-3612-4b54-b7a9-dfe718db2d99" />
