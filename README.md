# Aplicação Web: Sistema de Controle de Estoque - diAL

Aplicação web com CRUD desenvolvida com python, flask, sqlite e mongodb: 
  - Sistema de controle de estoque com controle de acesso e funcionalidades diferentes dependendo do nível do usuário

## Features

Nível do Usuário | Atualizar sua Própria Conta | Visualizar os Produtos | Adicionar um Produto | Editar um Produto | Deletar um Produto | Visualizar os Usuários | Adicionar um Usuário | Editar um Usuário | Deletar um Usuário
--- | --- | --- | --- |--- |--- |--- |--- |--- |---
User | <p align="center"> &#9745; </p> | <p align="center"> &#9745; </p> |  <p align="center"> &#9744; </p> | <p align="center"> &#9744; </p> | <p align="center"> &#9744; </p> | <p align="center"> &#9744; </p> | <p align="center"> &#9744; </p> | <p align="center"> &#9744; </p> | <p align="center"> &#9744; </p> | <p align="center"> &#9744; </p>
Admin | <p align="center"> &#9745; </p> | <p align="center"> &#9745; </p> | <p align="center"> &#9745; </p> | <p align="center"> &#9745; </p> | <p align="center"> &#9745; </p> | <p align="center"> &#9745; </p> | <p align="center"> &#9745; </p> | <p align="center"> &#9745; </p> | <p align="center"> &#9745; </p> | <p align="center"> &#9745; </p>

Novas contas criadas na aplicação terão o nível de usuário 'user' por padrão, a única maneira de elevar o nível para 'admin' é editando a conta do usuário pelo gerenciamento de usuários, funcionalidade que só é disponibilizada para usuários administradores.

- Usuário administrador padrão: login: admin, senha: admin.

## Demonstração:

