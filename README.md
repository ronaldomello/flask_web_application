# Aplicação Web: Sistema de Controle de Estoque - diAL

Aplicação web com CRUD desenvolvida com python, flask, sqlalchemy e mongodb: 
  - Sistema de controle de estoque e gerenciamento de usuários da aplicação com controle de acesso e funcionalidades diferentes dependendo do nível do usuário.

O controle de acesso é verificado em toda chamada GET ou POST nas rotas para verificar se o usuário tem o nível preciso para realizar a operação, se o usuário está logado em uma sessão e se o usuário está tentando acessar a sessão de outra pessoa.

Todo o código está extensamente comentado, possui templates html com estilizações em css. Os comentários do cógio foram feitos em inglês por preferência.

## Índice

- 1. [Features](https://github.com/bccalegari/flask_web_application#features)
- 2. [Demonstração](https://github.com/bccalegari/flask_web_application#demonstra%C3%A7%C3%A3o)
- 3. [Detalhamento](https://github.com/bccalegari/flask_web_application#detalhamento)
- 4. [Instalação](https://github.com/bccalegari/flask_web_application#instalação)
- 5. [Arquivos](https://github.com/bccalegari/flask_web_application#arquivos)
- 6. [Tecnologias Utilizadas](https://github.com/bccalegari/flask_web_application#tecnologias-utilizadas)

## Features

Nível do Usuário | Atualizar sua Própria Conta | Visualizar os Produtos | Adicionar um Produto | Editar um Produto | Deletar um Produto | Visualizar os Usuários | Adicionar um Usuário | Editar um Usuário | Deletar um Usuário
--- | --- | --- | --- |--- |--- |--- |--- |--- |---
User | <p align="center"> &#9745; </p> | <p align="center"> &#9745; </p> |  <p align="center"> &#9744; </p> | <p align="center"> &#9744; </p> | <p align="center"> &#9744; </p> | <p align="center"> &#9744; </p> | <p align="center"> &#9744; </p> | <p align="center"> &#9744; </p> | <p align="center"> &#9744; </p> | <p align="center"> &#9744; </p>
Admin | <p align="center"> &#9745; </p> | <p align="center"> &#9745; </p> | <p align="center"> &#9745; </p> | <p align="center"> &#9745; </p> | <p align="center"> &#9745; </p> | <p align="center"> &#9745; </p> | <p align="center"> &#9745; </p> | <p align="center"> &#9745; </p> | <p align="center"> &#9745; </p> | <p align="center"> &#9745; </p>

Novas contas criadas na aplicação terão o nível de usuário 'user' por padrão, a única maneira de elevar o nível para 'admin' é editando a conta do usuário pelo gerenciamento de usuários, funcionalidade que só é disponibilizada para usuários administradores.

- Usuário comum padrão: login: user, senha: user.
- Usuário administrador padrão: login: admin, senha: admin.

## Demonstração:

A demonstração geral foi limitada a duas funcionalidades, a visão do controle de inventário por um usuário comum, e a visão do administrador, incluindo o controle dos usuários da aplicação.

Visão geral usuário comum:

https://user-images.githubusercontent.com/109561086/215350987-25c0f9e0-fd13-4074-8819-66229edd47c2.mp4

Visão geral administrador:

https://user-images.githubusercontent.com/109561086/215351004-c28d4bc0-3594-4b85-bd0f-affe7dfdb742.mp4

### Demonstrações Detalhadas:

#### Sign Up - Erros:

https://user-images.githubusercontent.com/109561086/215351053-3f1333fb-cd02-43b9-9e0f-ad2d320ea521.mp4

#### Log In - Erros:

https://user-images.githubusercontent.com/109561086/215351063-d7a48f11-22a4-412e-b471-86d370ce9eec.mp4

#### Sign Up e Log In - Sucesso:

https://user-images.githubusercontent.com/109561086/215351097-4c7f97dc-61b6-4509-8a29-3359e788902f.mp4

#### Update Account - Erros:

https://user-images.githubusercontent.com/109561086/215351205-b71faafe-ecdb-4b6e-b7a3-8eb06fcb88d7.mp4

#### Update Account - Sucesso:

https://user-images.githubusercontent.com/109561086/215351229-65aeac6b-a05a-410b-90f9-08bc788c6ee4.mp4

#### Inventory Management:

- User:

https://user-images.githubusercontent.com/109561086/215351285-1cf04c85-445d-421d-a6f8-f41df053248d.mp4

- Admin:

  - Add - Erros:
  
  https://user-images.githubusercontent.com/109561086/215351362-d8c28a99-3140-4437-86c2-60b6225b8da4.mp4

  - Add - Sucesso:

  https://user-images.githubusercontent.com/109561086/215351584-a87b7136-c619-4b0c-8394-49bf12aee56e.mp4

  - Edit - Erros:

  https://user-images.githubusercontent.com/109561086/215351421-cfe3cc7b-69cb-44ba-8d03-c5ed8ce271e9.mp4

  - Edit - Sucesso:

  https://user-images.githubusercontent.com/109561086/215351431-51c09b8e-d1ed-4645-957d-c95d1692a0b4.mp4

  - Delete:

  https://user-images.githubusercontent.com/109561086/215351438-5f3d3b7c-b415-4377-aa8c-d6df02a5f295.mp4

#### User Management:

- Add - Erros:

https://user-images.githubusercontent.com/109561086/215351500-3be9167f-763f-41a5-84b6-b50f41a9244b.mp4

- Add - Sucesso:

https://user-images.githubusercontent.com/109561086/215351511-1d00b0df-ba73-4f0c-a8c4-3123dfa393d1.mp4

- Edit - Erros:

https://user-images.githubusercontent.com/109561086/215351516-f49267b3-2a41-4a27-9e20-44f92521d3db.mp4

- Edit - Sucesso:

https://user-images.githubusercontent.com/109561086/215351526-3c57b5bc-9d2a-4263-bee0-15abdb4d167a.mp4

- Delete:

https://user-images.githubusercontent.com/109561086/215351541-558e737f-68f0-490d-a7cb-3728417b68d5.mp4

## Detalhamento:

### Bancos de Dados:

Existem dois bancos de dados na aplicação, o primeiro é o SQLite que comporta os usuários (todas as senhas são submetidas a uma criptografia md5 para serem armazenadas no banco) da aplicação e o segundo o MongoDB que comporta os produtos da aplicação. Cada banco possui sua classe de utilidades, referentes a select, insert, update e delete, sendo o SqlUtils referente ao SQLite e o MongoUtils referente ao MongoDB, para um detalhamento maior de suas funcionalidades, verificar os comentários no código.

### Sign Up:

Funcionalidade para um usuário comum criar sua conta na aplicação, possui três tipos de travas diferentes:
-  1. Login(username) já existente na aplicação. (Login e e-mail são unique constraints no banco) // Retorno: "Username already exists."
-  2. E-mail já existente na aplicação. (Login e e-mail são unique constraints no banco) // Retorno: "E-mail already exists."
-  3. As senhas inseridas não coincidem. (Senha e confirmação de senha) // Retorno: "Password don't match."

### Log in:

Funcionalidade para um usuário logar na aplicação, possui dois tipos de travas diferentes:
-  1. O login inserido não existe. // Retorno: "User not found."
-  2. A senha inserida está incorreta. // Retorno: "Incorrect Password."

### Log in:

Funcionalidade para um usuário deslogar da aplicação, (por padrão, a sessão dura no máximo 30m, após isso o usuário será deslogado automaticamente).

### My Account:

Funcionalidade para um usuário visualizar informações sobre sua conta, retorna as seguintes informações:
-  1. Login
-  2. Name
-  2. E-mail

### Update my Account:

Funcionalidade para um usuário atualizar os dados da sua conta, permite modificar qualquer informação, mas necessita da senha atual para que a modificação seja feita. Possui quatro tipos de travas diferentes:
-  1. Login(username) já existente na aplicação. (Login e e-mail são unique constraints no banco) // Retorno: "Username already exists."
-  2. E-mail já existente na aplicação. (Login e e-mail são unique constraints no banco) // Retorno: "E-mail already exists."
-  3. As senhas inseridas não coincidem. (Senha e confirmação de senha) // Retorno: "Password don't match."
-  4. A senha inserida está incorreta. (Senha atual) // Retorno: "Incorrect Password."

### Inventory Management:

Funcionalidade para um usuário visualizar os produtos e seus estoques respectivos, caso o usuário seja administrador ele terá acesso a criação, edição e deleção de produtos. A tela possui a funcionalidade de pesquisa por um produto, sendo de match parcial, funcionando como uma consulta 'LIKE', caso o produto não seja encontrado, será retornado a mensagem "Product not found".

#### Usuário Administrador:

##### Inventory Add:

Funcionalidade para um usuário admistrador adicionar um novo produto, o id do usuário será armazenado no registro do produto, possui apenas uma única trava, relacionada a unicidade do registro, constraint unique composta -> [nome do produto, código do produto, endereço do inventário]
-  1. O produto já existe no inventário(nome, código, endereço do inventário). (unique constraint composta) // Retorno: "Product already exists in this stock."

##### Inventory Edit:

Funcionalidade para um usuário admistrador editar um produto, o id do usuário será atualizado para o id de quem está atualizando no registro do produto, possui apenas uma única trava, relacionada a unicidade do registro, constraint unique composta -> [nome do produto, código do produto, endereço do inventário]
-  1. O produto já existe no inventário(nome, código, endereço do inventário). (unique constraint composta) // Retorno: "Product already exists in this stock."

##### Inventory Delete:

Funcionalidade para um usuário admistrador deletar um produto.

### User Management:

Funcionalidade para um usuário administrador visualizar, criar, editar e deletar os usuários da aplicação. A tela possui a funcionalidade de pesquisa por um usuário, sendo de match parcial, funcionando como uma consulta 'LIKE', caso o usuário não seja encontrado, será retornado a mensagem "User not found".

##### User Add:

Funcionalidade para um usuário admistrador adicionar um novo usuário, possibilitando a escolha do nível do usuário, possui as mesmas travas que a criação de uma conta possuem:
-  1. Login(username) já existente na aplicação. (Login e e-mail são unique constraints no banco) // Retorno: "Username already exists."
-  2. E-mail já existente na aplicação. (Login e e-mail são unique constraints no banco) // Retorno: "E-mail already exists."
-  3. As senhas inseridas não coincidem. (Senha e confirmação de senha) // Retorno: "Password don't match."

##### User Edit:

Funcionalidade para um usuário admistrador editar as informações de um usuário, possui as mesmas travas que a criação de uma conta possuem:
-  1. Login(username) já existente na aplicação. (Login e e-mail são unique constraints no banco) // Retorno: "Username already exists."
-  2. E-mail já existente na aplicação. (Login e e-mail são unique constraints no banco) // Retorno: "E-mail already exists."
-  3. As senhas inseridas não coincidem. (Senha e confirmação de senha) // Retorno: "Password don't match."

##### User Delete:

Funcionalidade para um usuário admistrador deletar um usuário.

## Instalação:

Para rodar o código em sua máquina será necessário criar uma conta no site [MongoDB Atlas](https://www.mongodb.com/cloud/atlas/register), realize a conexão com seu cluster substituindo o código de conexão na linha 9 do arquivo 'mongodb.py' pelo seu.

## Arquivos:

dial_web_development_flask:
- static -> arquivos css referentes aos templates html.
- templates -> templates html.
- app.py -> arquivo principal, adiciona todas as rotas ao app, executar para ligar o app.
- config.py -> arquivo de configurações do servidor.
- diAL_users.db -> banco de dados gerado pelo arquivo 'models.py', contém os usuários da aplicação.
- models.py -> arquivo de criação do banco de dados, contém o modelo da tabela de usuários.
- mongodb.py -> arquivo de instanciação e conexão com o MongoDB Atlas, também contém operações de utilidade (CRUD).
- sql_utils.py -> arquivo de utilidade para manipular o banco de dados, contém operações de CRUD.
- routes.py -> contém todas as rotas da aplicação com suas respectivas regras de negócio.

## Tecnologias Utilizadas:

Tecnologia | Versão
--- | ---
Python | 3.10.4
Flask | 2.2.2
Flask-RESTful | 0.3.9
pymongo | 4.3.3
SQLAlchemy | 1.4.42
