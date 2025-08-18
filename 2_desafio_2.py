from datetime import datetime

class Transacao:
    def __init__(self, valor):
        self.valor = valor
        self.data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

class Deposito(Transacao):
    def registrar(self, conta):
        conta.saldo += self.valor
        conta.historico.adicionar(self)
        print(f"\n✅ Depósito de R$ {self.valor:.2f} realizado com sucesso!")

class Saque(Transacao):
    def registrar(self, conta):
        if self.valor > conta.saldo:
            print("\n❌ Operação falhou! Saldo insuficiente.")
        elif self.valor > conta.limite:
            print("\n❌ Operação falhou! Valor acima do limite permitido.")
        elif conta.numero_saques >= conta.limite_saques:
            print("\n❌ Operação falhou! Limite diário de saques atingido.")
        elif self.valor > 0:
            conta.saldo -= self.valor
            conta.numero_saques += 1
            conta.historico.adicionar(self)
            print(f"\n✅ Saque de R$ {self.valor:.2f} realizado com sucesso!")
        else:
            print("\n❌ Operação falhou! Valor inválido.")


class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar(self, transacao):
        self.transacoes.append(transacao)


class Conta:
    def __init__(self, numero, cliente, agencia="0001"):
        self.numero = numero
        self.agencia = agencia
        self.cliente = cliente
        self.saldo = 0
        self.limite = 500
        self.numero_saques = 0
        self.limite_saques = 3
        self.historico = Historico()

    def depositar(self, valor):
        if valor > 0:
            deposito = Deposito(valor)
            deposito.registrar(self)
        else:
            print("\n❌ Operação falhou! Valor inválido.")

    def sacar(self, valor):
        saque = Saque(valor)
        saque.registrar(self)

    def exibir_extrato(self):
        print("\n================ EXTRATO ================")
        print(f"Titular: {self.cliente.nome} | CPF: {self.cliente.cpf}")
        print(f"Conta nº {self.numero} | Agência {self.agencia}")
        print("------------------------------------------")

        if not self.historico.transacoes:
            print("Não foram realizadas movimentações.")
        else:
            for t in self.historico.transacoes:
                print(f"{t.__class__.__name__}: R$ {t.valor:.2f} em {t.data}")

        print("------------------------------------------")
        print(f"Saldo: R$ {self.saldo:.2f}")
        print("==========================================")


class Cliente:
    def __init__(self, nome, cpf, data_nascimento, endereco):
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.endereco = endereco
        self.contas = []

    def adicionar_conta(self, conta):
        self.contas.append(conta)


def filtrar_cliente(cpf, clientes):
    for cliente in clientes:
        if cliente.cpf == cpf:
            return cliente
    return None

def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente números): ").strip()
    if filtrar_cliente(cpf, clientes):
        print("\n❌ Já existe cliente com este CPF!")
        return clientes

    nome = input("Informe o nome completo: ").strip()
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ").strip()
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ").strip()

    cliente = Cliente(nome, cpf, data_nascimento, endereco)
    clientes.append(cliente)
    print("\n✅ Cliente criado com sucesso!")
    return clientes

def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ").strip()
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        conta = Conta(numero_conta, cliente)
        cliente.adicionar_conta(conta)
        contas.append(conta)
        print("\n✅ Conta criada com sucesso!")
        return numero_conta + 1, contas
    else:
        print("\n❌ Cliente não encontrado! Criação de conta encerrada.")
        return numero_conta, contas

def listar_contas(clientes):
    if not clientes:
        print("\nNenhum cliente cadastrado.")
        return

    for cliente in clientes:
        if not cliente.contas:
            continue
        print(f"\nCliente: {cliente.nome} | CPF: {cliente.cpf}")
        for conta in cliente.contas:
            print(f"  Agência: {conta.agencia} | Conta: {conta.numero} | Saldo: R$ {conta.saldo:.2f}")

def main():
    clientes = []
    contas = []
    numero_conta = 1

    menu = """
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [nc] Novo Cliente
    [cc] Criar Conta
    [lc] Listar Contas
    [q] Sair
    => """

    while True:
        opcao = input(menu).lower().strip()

        if opcao == "d":
            cpf = input("Informe o CPF do cliente: ").strip()
            cliente = filtrar_cliente(cpf, clientes)
            if not cliente or not cliente.contas:
                print("\n❌ Cliente não possui conta!")
                continue
            valor = float(input("Informe o valor do depósito: "))
            cliente.contas[0].depositar(valor)  # usa a primeira conta

        elif opcao == "s":
            cpf = input("Informe o CPF do cliente: ").strip()
            cliente = filtrar_cliente(cpf, clientes)
            if not cliente or not cliente.contas:
                print("\n❌ Cliente não encontrado ou não possui conta!")
                continue
            valor = float(input("Informe o valor do saque: "))
            cliente.contas[0].sacar(valor)

        elif opcao == "e":
            cpf = input("Informe o CPF do cliente: ").strip()
            cliente = filtrar_cliente(cpf, clientes)
            if not cliente or not cliente.contas:
                print("\n❌ Cliente não encontrado ou não possui conta!")
                continue
            cliente.contas[0].exibir_extrato()

        elif opcao == "nc":
            clientes = criar_cliente(clientes)

        elif opcao == "cc":
            numero_conta, contas = criar_conta(numero_conta, clientes, contas)

        elif opcao == "lc":
            listar_contas(clientes)

        elif opcao == "q":
            print("\nSaindo do sistema... Até logo!")
            break

        else:
            print("\n❌ Opção inválida, tente novamente.")

if __name__ == "__main__":
    main()

