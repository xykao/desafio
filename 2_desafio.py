def depositar(saldo, valor, extrato, /):
    """Função para depósito (argumentos por posição)."""
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        print("\n✅ Depósito realizado com sucesso!")
    else:
        print("\n❌ Operação falhou! O valor informado é inválido.")
    return saldo, extrato


def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    """Função para saque (argumentos keyword only)."""
    if valor > saldo:
        print("\n❌ Operação falhou! Saldo insuficiente.")
    elif valor > limite:
        print("\n❌ Operação falhou! Valor acima do limite permitido.")
    elif numero_saques >= limite_saques:
        print("\n❌ Operação falhou! Limite diário de saques atingido.")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        print("\n✅ Saque realizado com sucesso!")
    else:
        print("\n❌ Operação falhou! O valor informado é inválido.")

    return saldo, extrato, numero_saques


def exibir_extrato(saldo, /, *, extrato):
    """Função para exibir extrato (posicional + keyword)."""
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")


def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente números): ").strip()
    usuario = filtrar_usuario(cpf, usuarios)
    if usuario:
        print("\n❌ Já existe usuário com este CPF!")
        return usuarios

    nome = input("Informe o nome completo: ").strip()
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ").strip()
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ").strip()

    usuarios.append({
        "nome": nome,
        "data_nascimento": data_nascimento,
        "cpf": cpf,
        "endereco": endereco
    })
    print("\n✅ Usuário criado com sucesso!")
    return usuarios


def filtrar_usuario(cpf, usuarios):
    """Retorna o usuário com o CPF informado ou None."""
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def criar_conta(agencia, numero_conta, usuarios, contas):
    cpf = input("Informe o CPF do usuário: ").strip()
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        conta = {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
        contas.append(conta)
        print("\n✅ Conta criada com sucesso!")
        return contas
    else:
        print("\n❌ Usuário não encontrado! Criação de conta encerrada.")
        return contas


def listar_contas(contas):
    if not contas:
        print("\nNenhuma conta cadastrada.")
    for conta in contas:
        print(f"""
Agência: {conta['agencia']}
Conta: {conta['numero_conta']}
Titular: {conta['usuario']['nome']}
""")


def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    numero_conta = 1

    usuarios = []
    contas = []

    menu = """
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [nu] Novo Usuário
    [nc] Nova Conta
    [lc] Listar Contas
    [q] Sair
    => """

    while True:
        opcao = input(menu).lower().strip()

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))
            saldo, extrato, numero_saques = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES
            )

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "nu":
            usuarios = criar_usuario(usuarios)

        elif opcao == "nc":
            contas = criar_conta(AGENCIA, numero_conta, usuarios, contas)
            if len(contas) >= numero_conta:
                numero_conta += 1

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            print("\nSaindo do sistema... Até logo!")
            break

        else:
            print("\n❌ Opção inválida, tente novamente.")


if __name__ == "__main__":
    main()
