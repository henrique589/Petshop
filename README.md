# 🐾 Sistema de Gerenciamento de Pet Shop

Este projeto é um sistema de gerenciamento para um Pet Shop, desenvolvido em **Python** utilizando o padrão de arquitetura **MVC (Model-View-Controller)**. O sistema visa facilitar a organização de serviços, cadastros, vendas e agendamentos realizados em um ambiente de Pet Shop.

---

```cpp
#define AUTHOR ["Eduardo Monteiro Costa Pires"]
#define AUTHOR ["Gabriel Souza de Oliveira"]
#define AUTHOR ["Henrique Azevedo Andrade Silva"]
#define AUTHOR ["Lucas Mendonça Sacchi"]
```

```cpp
#define Professor ["Elder José Reioli Cirilo"]
```

---

## 🚀 Funcionalidades

O sistema contempla as seguintes funcionalidades, descritas inicialmente em **histórias de usuário**:

### 👤 Clientes
- Cadastro de dados pessoais (nome, e-mail, telefone, CPF)
- Cadastro de pets vinculados a um cliente
- Login básico por CPF

### 🧾 Vendas e Produtos
- Cadastro e atualização de catálogo de produtos e serviços

### 🧑‍💼 Gestão Interna
- Cadastro e gerenciamento de funcionários

---

## 🧱 Arquitetura

O projeto segue o padrão **MVC**, com as seguintes responsabilidades:

- **Model**: representa as entidades do sistema
- **View**: coleta e exibe dados ao usuário por meio da interface gráfica
- **Controller**: coordena o fluxo entre Model, View e banco
- **DAO**: acesso ao banco de dados usando **SQLite3**

---

## ▶️ Como executar

1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/petshop-system.git
cd petshop-system

---

## 🔄 Metodologia SCRUM

O desenvolvimento do sistema é orientado por práticas ágeis, utilizando o **framework SCRUM**

### 🛠️ Gestão de tarefas
- Ferramenta: **Jira**
- Tarefas organizadas por histórias de usuário e categorizadas por épicos
- Uso de board Kanban com colunas: _A Fazer_, _Em Progresso_, _Em Validação_, _Concluído_