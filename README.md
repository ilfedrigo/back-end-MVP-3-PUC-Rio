# UrbanTrendz Backend

O UrbanTrendz Backend é responsável por gerenciar as operações relacionadas a compras, autenticação de usuários e interações com o banco de dados.

O back-end implementa rotas com Flask e Banco de Dados com SQLite3

## Arquitetura

<img width="441" alt="Screenshot 2024-04-25 at 11 08 04" src="https://github.com/ilfedrigo/back-end-MVP-3-PUC-Rio/assets/115956776/7b73864b-1f46-439f-8a97-75de59213e6b">

## Instruções de instalação

Para rodar o backend, siga os passos abaixo:

1. Certifique-se de ter o Docker instalado em sua máquina.
2. Clone este repositório para o seu ambiente local.
3. No terminal, navegue até a pasta do backend.
4. Execute o seguinte comando para construir e rodar o container Docker:

```bash
docker build -t urbantrendz-backend .
docker run -p 5006:5006 urbantrendz-backend
```

5. O backend estará disponível em [http://localhost:5006](http://localhost:5006).

## Arquivos do projeto

- **main.py**: Contém a lógica principal do backend, incluindo rotas, operações de banco de dados e autenticação de usuários.
- **Dockerfile**: Utilizado para construir a imagem do Docker do backend.

## Funcionalidades e Rotas

### Rotas Principais:

1. **/** (`login_page`):
   - Esta rota renderiza a página de login em HTML. Os usuários podem inserir suas credenciais de login nesta página.

2. **/checkout** (`checkout`):
   - Método: POST
   - Esta rota é responsável por processar o checkout dos itens adicionados ao carrinho. Os dados do carrinho são enviados como JSON no corpo da solicitação. Os itens do carrinho são inseridos no banco de dados, juntamente com o ID do usuário e o total da compra. Após a conclusão bem-sucedida do checkout, uma mensagem de confirmação é retornada.

3. **/orders** (`orders`):
   - Método: GET
   - Esta rota retorna uma lista de todas as ordens de compra registradas no banco de dados. Cada ordem contém o ID do item, o nome do item e o preço.

4. **/orders/<item_id>** (`delete_order` e `edit_order`):
   - Método: DELETE (delete_order), PUT (edit_order)
   - `/orders/<item_id>` é uma rota dinâmica que permite a exclusão (DELETE) e atualização (PUT) de um item específico do banco de dados com base no seu ID.
   - Perceba que o botão **EDIT** ainda não foi completamente implementado.

5. **/login** (`login`):
   - Método: POST
   - Esta rota é responsável por autenticar os usuários. Os dados de login (nome de usuário e senha) são enviados como JSON no corpo da solicitação. Se as credenciais forem válidas, o usuário é redirecionado para a página de administração (admin.html) ou para a página inicial (index.html), dependendo do tipo de usuário (admin ou não admin).

6. **/signup** (`signup`):
   - Método: POST
   - Esta rota é responsável por criar novos usuários. Os dados do novo usuário (nome de usuário e senha) são enviados como JSON no corpo da solicitação. Se o nome de usuário fornecido não estiver em uso, o novo usuário é adicionado ao banco de dados e uma mensagem de confirmação é retornada.

### Funcionalidades Adicionais:

- As rotas são protegidas contra vulnerabilidades de segurança, como solicitações de mídia não suportadas.
- A comunicação entre o frontend e o backend é permitida através da habilitação do Cross-Origin Resource Sharing (CORS) utilizando a extensão Flask-CORS.

Essas rotas fornecem a funcionalidade essencial para o funcionamento do UrbanTrendz Backend, permitindo que os usuários autentiquem-se, realizem compras, gerenciem seus carrinhos e visualizem e manipulem as ordens de compra.

---
