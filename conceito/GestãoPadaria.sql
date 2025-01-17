-- Criar banco de dados
CREATE DATABASE bd_padaria;
USE bd_padaria;

-- Tabela de usuários
CREATE TABLE tb_usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    telefone VARCHAR(15),  -- Adiciona o campo de telefone
    tipo_usuario ENUM('Administrador', 'Funcionario') NOT NULL,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	primeiro_login BOOLEAN DEFAULT TRUE
);

-- Tabela de fornecedores
CREATE TABLE tb_fornecedores (
    id_fornecedor INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    telefone VARCHAR(15),
    email VARCHAR(100),
    endereco TEXT,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de categorias de produtos
CREATE TABLE tb_categorias (
    id_categoria INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    descricao TEXT,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de produtos
CREATE TABLE tb_produtos (
    id_produto INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    id_categoria INT,
    preco DECIMAL(10,2) NOT NULL,
    quantidade_estoque INT NOT NULL,
    id_fornecedor INT,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_categoria) REFERENCES tb_categorias(id_categoria) ON DELETE SET NULL,
    FOREIGN KEY (id_fornecedor) REFERENCES tb_fornecedores(id_fornecedor) ON DELETE SET NULL
);

-- Tabela de pedidos internos
CREATE TABLE tb_pedidos_internos (
    id_pedido INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    data_pedido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('Pendente', 'Em Produção', 'Concluído') DEFAULT 'Pendente',
    FOREIGN KEY (id_usuario) REFERENCES tb_usuarios(id_usuario) ON DELETE CASCADE
);

-- Tabela de itens do pedido interno
CREATE TABLE tb_itens_pedido_interno (
    id_item INT AUTO_INCREMENT PRIMARY KEY,
    id_pedido INT NOT NULL,
    id_produto INT NOT NULL,
    quantidade INT NOT NULL,
    FOREIGN KEY (id_pedido) REFERENCES tb_pedidos_internos(id_pedido) ON DELETE CASCADE,
    FOREIGN KEY (id_produto) REFERENCES tb_produtos(id_produto) ON DELETE CASCADE
);

-- Tabela de transações financeiras
CREATE TABLE tb_transacoes (
    id_transacao INT AUTO_INCREMENT PRIMARY KEY,
    tipo ENUM('Venda', 'Despesa') NOT NULL,
    descricao TEXT,
    valor DECIMAL(10,2) NOT NULL,
    data_transacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de vendas
CREATE TABLE tb_vendas (
    id_venda INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    total DECIMAL(10,2) NOT NULL,
    data_venda TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES tb_usuarios(id_usuario) ON DELETE CASCADE
);

-- Tabela de itens da venda
CREATE TABLE tb_itens_venda (
    id_item INT AUTO_INCREMENT PRIMARY KEY,
    id_venda INT NOT NULL,
    id_produto INT NOT NULL,
    quantidade INT NOT NULL,
    preco_unitario DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (id_venda) REFERENCES tb_vendas(id_venda) ON DELETE CASCADE,
    FOREIGN KEY (id_produto) REFERENCES tb_produtos(id_produto) ON DELETE CASCADE
);