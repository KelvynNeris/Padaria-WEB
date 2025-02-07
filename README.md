# Padaria WEB

O **Padaria WEB** é um sistema web para gerenciamento de uma padaria, desenvolvido para facilitar o controle de vendas, estoque e transações fiadas, além de gerar relatórios detalhados sobre itens, categorias e métodos de pagamento. O sistema também inclui um módulo específico para o controle de fiado, permitindo acompanhar o valor total fiado, os pagamentos realizados e o saldo pendente.

---

## Funcionalidades

- **Cadastro e Gerenciamento de Produtos:**  
  Permite cadastrar, editar e remover produtos. Os produtos podem ser vendidos por unidade ou por quilo, com atualização automática do estoque e cálculo dos valores.

- **Registro de Vendas:**  
  Registra vendas com diferentes métodos de pagamento (Dinheiro, Cartão, Pix, Fiado) e gera relatórios detalhados.

- **Gestão de Fiado:**  
  Permite registrar transações fiadas e atualizar pagamentos via AJAX. O sistema calcula o total fiado, os valores pagos e o saldo pendente.

- **Relatórios Dinâmicos:**  
  Relatórios com filtros por data, quantidade vendida e total arrecadado, oferecendo uma visão detalhada do desempenho da padaria.

- **Interface Responsiva e Moderna:**  
  Design com animações suaves e paleta de cores inspirada em padarias, garantindo uma experiência agradável em qualquer dispositivo.

---

## Tecnologias Utilizadas

- **Backend:** Python, Flask  
- **Banco de Dados:** MySQL  
- **Frontend:** HTML, CSS, JavaScript, jQuery, Select2  
- **Templates:** Jinja2

---

## Passo a Passo para Instalação e Configuração

### Pré-requisitos

- [Python 3.x](https://www.python.org/downloads/)
- [MySQL Server](https://dev.mysql.com/downloads/mysql/)
- Git

### 1. Clone o Repositório

Abra o terminal e execute:

```bash
git clone https://github.com/seu-usuario/padaria-gestao.git
cd padaria-gestao
```
### 2. Crie e Ative um Ambiente Virtual

```bash
python -m venv venv
```

- No Linux/Mac:

```bash
source venv/bin/activate
```

- No Windows:

```bash
venv\Scripts\activate
```

### 3. Instale as Dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o Banco de Dados

- Crie um banco de dados MySQL (por exemplo, padaria_gestao).
- Execute os scripts SQL disponíveis na pasta database para criar as tabelas necessárias (ex.: tb_vendas, tb_produtos, tb_clientes_fiado, etc.).
- Atualize as configurações de conexão no arquivo config.py com os parâmetros do seu banco de dados.

## Estrutura do Projeto

```csharp
padaria-gestao/
├── app.py                  # Arquivo principal do Flask
├── config.py               # Configurações do projeto (ex.: conexão com o banco de dados)
├── requirements.txt        # Dependências do projeto
├── templates/              # Templates HTML (ex.: modelo.html, relatorio_mais_vendidos.html, relatorio_fiado.html, etc.)  
├── static/                 # Arquivos estáticos\n│   ├── css/            # Arquivos CSS\n│   ├── js/             # Arquivos JavaScript\n│   └── images/         # Imagens e ícones\n└── database/            # Scripts SQL para criação do banco de dados
```

### Fluxo de Trabalho

## 1. Cadastro de Produtos:

- Adicione, edite ou remova produtos do estoque.
- Defina se o produto é vendido por unidade ou por quilo, com os respectivos preços.

## 2. Registro de Vendas:

- Selecione os produtos e registre as vendas.
- Escolha o método de pagamento, incluindo a opção "Fiado" para transações a prazo.

## 3. Gestão de Fiado:

- Acesse o relatório de fiado para visualizar as transações pendentes.
- Utilize o formulário com AJAX para atualizar os pagamentos das transações fiadas.
- O sistema calcula automaticamente o total fiado, o valor pago e o saldo pendente.

## 4. Relatórios Dinâmicos

- Visualize relatórios com filtros por data, quantidade vendida e total arrecadado.
- Analise o desempenho dos produtos, categorias e métodos de pagamento.

## 5. Cadastro de Usuários e Funcionários:

- O usuário master, que já está previamente cadastrado no banco, pode acessar e alterar suas informações pessoais.
- Funcionários podem enviar pedidos de cadastro, que serão gerenciados e aprovados pelo sistema.

### Funcionalidades Adicionais

## 1. Atualização via AJAX:
- Permite atualizar os pagamentos das transações fiadas sem recarregar a página, com feedback imediato ao usuário.

## 2. Filtros Dinâmicos:
- Relatórios com filtros por data, quantidade vendida e total arrecadado, permitindo uma análise detalhada do desempenho da padaria.

## 3. Design Inspirado na Paleta de Cores da Padaria:
- Cores quentes, aconchegantes e animações suaves para uma experiência visual agradável e moderna.
