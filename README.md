# Daily Diet API 🥗

API desenvolvida como parte do desafio do módulo **Desenvolvimento Avançado com Flask** da Rocketseat.

## 📌 Sobre o projeto

A **Daily Diet API** é uma aplicação para controle de dieta diária, permitindo que usuários registrem e gerenciem suas refeições. Os dados são persistidos em um banco de dados SQLite utilizando SQLAlchemy.

## 🚀 Funcionalidades

- **Registrar** uma refeição com nome, descrição, data/hora e indicação se está dentro ou não da dieta
- **Listar** todas as refeições cadastradas
- **Visualizar** os detalhes de uma refeição específica
- **Editar** uma refeição existente
- **Excluir** uma refeição
- **WebSocket** configurado para comunicação em tempo real

## 🛠 Tecnologias

- Python 3.11
- Flask
- Flask-SQLAlchemy
- Flask-CORS
- Flask-SocketIO
- SQLite

## 📡 Endpoints da API

| Método | Rota | Descrição |
|--------|------|-----------|
| `POST` | `/refeicoes` ou `/created` | Cria uma nova refeição |
| `GET` | `/refeicoes` | Lista todas as refeições |
| `GET` | `/refeicoes/<id>` | Retorna os detalhes de uma refeição específica |
| `PUT` | `/refeicoes/<id>` ou `/refeicoes/update/<id>` | Atualiza uma refeição existente |
| `DELETE` | `/refeicoes/<id>` | Remove uma refeição |

### Exemplo de payload

```json
{
  "name": "Café da manhã",
  "description": "Ovos e frutas",
  "date_time": "2025-06-15 08:00:00",
  "in_diet": true
}
```

> O campo `date_time` deve estar no formato `YYYY-MM-DD HH:MM:SS`.

## 🏗 Estrutura do projeto

```
daily-diet-api/
├── src/
│   ├── app.py                  # Aplicação Flask e rotas
│   ├── db_models/
│   │   └── refeicoes.py        # Modelo da tabela Refeicoes
│   ├── repository/
│   │   └── database.py         # Instância do SQLAlchemy
│   └── instance/
│       └── database.db         # Banco de dados SQLite
├── requirements.txt            # Dependências do projeto
├── runtime.txt                 # Versão do Python para deploy
├── .render.yaml                # Configuração de deploy no Render
└── README.md                   # Documentação do projeto
```


## 🌐 Deploy

O projeto possui configuração para deploy no Render via arquivo `.render.yaml`:

- **Build:** `pip install -r requirements.txt`
- **Start:** `python src/app.py`
- **Python version:** 3.11.9
