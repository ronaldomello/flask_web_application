# Aplicação Web: Sistema de Controle de Estoque - diAL

Aplicação web com CRUD desenvolvida com python, flask, sqlite e mongodb: 
  - Sistema de controle de estoque com controle de acesso e funcionalidades diferentes dependendo do nível do usuário.

O controle de acesso é verificado em toda chamada GET ou POST nas rotas para verificar se o usuário tem o nível preciso para realizar a operação, se o usuário está logado em uma sessão e se o usuário está tentando acessar a sessão de outra pessoa.

Todo o código está extensamente comentado, o app, routes, config, models, sql_utils e mongodb. Possui templates html com estilizações em css. Os comentários estão em inglês por preferência. (Como estou buscando me aperfeiçoar em inglês, busco fazer os comentários em inglês em meus códigos)

## Features

Nível do Usuário | Atualizar sua Própria Conta | Visualizar os Produtos | Adicionar um Produto | Editar um Produto | Deletar um Produto | Visualizar os Usuários | Adicionar um Usuário | Editar um Usuário | Deletar um Usuário
--- | --- | --- | --- |--- |--- |--- |--- |--- |---
User | <p align="center"> &#9745; </p> | <p align="center"> &#9745; </p> |  <p align="center"> &#9744; </p> | <p align="center"> &#9744; </p> | <p align="center"> &#9744; </p> | <p align="center"> &#9744; </p> | <p align="center"> &#9744; </p> | <p align="center"> &#9744; </p> | <p align="center"> &#9744; </p> | <p align="center"> &#9744; </p>
Admin | <p align="center"> &#9745; </p> | <p align="center"> &#9745; </p> | <p align="center"> &#9745; </p> | <p align="center"> &#9745; </p> | <p align="center"> &#9745; </p> | <p align="center"> &#9745; </p> | <p align="center"> &#9745; </p> | <p align="center"> &#9745; </p> | <p align="center"> &#9745; </p> | <p align="center"> &#9745; </p>

Novas contas criadas na aplicação terão o nível de usuário 'user' por padrão, a única maneira de elevar o nível para 'admin' é editando a conta do usuário pelo gerenciamento de usuários, funcionalidade que só é disponibilizada para usuários administradores.

- Usuário administrador padrão: login: admin, senha: admin.

## Demonstração:

Limitei a demonstração geral a duas funcionalidades, a visão do controle de inventário por um usuário comum, e a visão do administrador, incluindo o controle dos usuários da aplicação, deixarei uma visualização mais detalhada de cada funcionalidade abaixo com gifs e prints.

Visão geral usuário comum:


Visão geral administrador:

- Controle de Inventário:

- Controle de Usuários:


## Detalhamento:

### Bancos de Dados:

Existem dois bancos de dados na aplicação, o primeiro é o SQLite que comporta os usuários da aplicação e o segundo o MongoDB que comporta os produtos da aplicação. Cada banco possui sua classe de utilidades, referentes a select, insert, update e delete, sendo o SqlUtils referente ao SQLite e o MongoUtils referente ao MongoDB, para um detalhamento maior de suas funcionalidades, verificar os comentários no código.

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
