# Daily Diet API 🥗  

API desenvolvida como parte do desafio do módulo **Desenvolvimento Avançado com Flask** da Rocketseat.  

## 📌 Sobre o projeto  

A **Daily Diet API** é uma aplicação para controle de dieta diária, permitindo que usuários registrem e gerenciem suas refeições.  

### 🚀 Funcionalidades  

✅ Registrar uma refeição com:  
- Nome  
- Descrição  
- Data e Hora  
- Indicação se está dentro ou não da dieta  

✅ Editar uma refeição existente  
✅ Excluir uma refeição  
✅ Listar todas as refeições de um usuário  
✅ Visualizar os detalhes de uma refeição específica  
✅ Armazenamento das informações em um banco de dados  

## 🛠 Tecnologias  

- Python 🐍  
- Flask ⚡  
- SQLite


# -------------------------------------------

Criar o ambiente Flask.
Configurar o banco de dados com SQLAlchemy.
Criar os endpoints da API:
    - Registrar uma refeição (POST /refeicoes)
    - Editar uma refeição (PUT /refeicoes/<id>)
    - Excluir uma refeição (DELETE /refeicoes/<id>)
    - Listar todas as refeições (GET /refeicoes)
    - Obter detalhes de uma refeição específica (GET /refeicoes/<id>)