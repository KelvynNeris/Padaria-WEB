# Padaria Gestão

O **Padaria Gestão** é um sistema web para gerenciamento de uma padaria, desenvolvido para facilitar o controle de vendas, estoque e transações fiadas, além de gerar relatórios detalhados sobre itens, categorias e métodos de pagamento. O sistema também inclui um módulo específico para o controle de fiado, permitindo acompanhar o valor total fiado, os pagamentos realizados e o saldo pendente.

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
