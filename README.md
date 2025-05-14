# 🐾 Sistema de Gerenciamento de Pet Shop

Este projeto é um sistema de gerenciamento para um Pet Shop, desenvolvido em **Python** utilizando o padrão de arquitetura **MVC (Model-View-Controller)**. O sistema visa facilitar a organização de serviços, cadastros, vendas e agendamentos realizados em um ambiente de Pet Shop.

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

- **Model**: representa as entidades do sistema (ex: Cliente, Pet)
- **View**: coleta e exibe dados ao usuário via terminal (CLI)
- **Controller**: coordena o fluxo entre Model, View e banco
- **DAO**: acesso ao banco de dados usando **SQLite3**

---

## ▶️ Como executar

1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/petshop-system.git
cd petshop-system