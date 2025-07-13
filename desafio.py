menu = """

[1] Depositar
[2] Sacar
[3] Extrato
[0] Sair

Escolha uma opção: """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:

    opcao = input(menu)

    if opcao == "1":
        print("Depósito")
        valor = float(input("Informe o valor do depósito: "))

        if valor > 0:
            saldo += valor
            extrato += f"Depósito: R$ {valor:.2f}\n"
        else:
            print("Operação falhou! O valor informado é invalido.")

    elif opcao == "2":
        print("Saque")
        valor = float(input("Informe o valor do saque: "))

        excedeu_saldo = valor > saldo
        
        excedeu_limite = valor > limite

        excedeu_saques = numero_saques >= LIMITE_SAQUES

        if excedeu_saldo:
            print("Operação falhou! Você não tem saldo suficiente.")

        elif excedeu_limite:
            print("Operação falhou! Você não tem limite suficiente.")

        elif excedeu_saques:
            print("Operação falhou! Você atingiu o número máximo de saques diários.")

        elif valor > 0:
            saldo -= valor
            extrato += f"Saque: R$ {valor:.2f}\n"
            numero_saques += 1

        else:
            print("Operção falhou! O valor informado é invalido.")
                   
    elif opcao == "3":

        print("\n--------------Extrato--------------")
        print("\nNão foram realizadas movimentações." if not extrato else extrato)
        print(f"\nSaldo: R$ {saldo:.2f}")
        print("-----------------------------------")
               
    elif opcao == "0":
        print("Sair")
        break
    else:
        print("Operação inválida, selecione a operação desejada.")
        