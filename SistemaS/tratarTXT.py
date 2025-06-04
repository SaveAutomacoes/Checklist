def main(caminho_planilha_modelo, caminho_arquivo, caminho_pasta_cliente, cnpj):
    '''
    caminho_planilha_modelo: Caminho do arquivo Excel modelo que contém o cabeçalho com os códigos de pagamento.
    caminho_arquivo: Caminho do arquivo PDF que contém os comprovantes de pagamento.
    caminho_pasta_cliente: Caminho da pasta onde o arquivo Excel será salvo após o preenchimento.
    cnpj: CNPJ do cliente, usado para nomear o arquivo Excel salvo.
    '''
    import PyPDF2
    import re
    import openpyxl

    # Aba da planilha modelo onde serão colados os pagamento
    aba_planilha_modelo = 'Base Dados (Colar Aqui Pgmtos)'

    # Abre o arquivo Excel
    wb = openpyxl.load_workbook(caminho_planilha_modelo)
    ws = wb[aba_planilha_modelo]

    # Pega o cabeçalho da planilha modelo com openpyxl
    itensCabecalho = [cell.value for cell in ws[1]]

    # Lista para armazenar os itens do cabeçalho formatados
    itensCabecalhoFormatado = [] 

    # Formata o cabeçalho da planilha modelo
    for cont, item in enumerate(itensCabecalho):
        if cont > 0:
            # Pega apenas os 5 primeiros caracteres do item
            item = item[:7]
            itensCabecalhoFormatado.append(item)

    # Lista do resultado
    listaResultado = []

    # Abre o PDF
    arquivoPDF = open(caminho_arquivo, 'rb')

    # Cria um objeto em PDF
    arquivoPDF = PyPDF2.PdfReader(arquivoPDF)

    # Para cada página do PDF
    for pagina in arquivoPDF.pages:

        # Extrai o texto da página
        texto = pagina.extract_text()
        

        # Capturar as Datas:
        padrao = r"(\d{2}/\d{2}/\d{4})\s+(\d{2}/\d{2}/\d{4})"
        resultado_REGEX = re.search(padrao, texto)
        apuracao, vencimento = resultado_REGEX.groups()


        # Captura os pagamentos:
        padrao = r"(\d{4})\s+[^\d\n]+?\s+([\d.,]+).*?\n.*?([\d.,]+)"
        resultado_REGEX = re.findall(padrao, texto) # Ele salva em uma tupla, sendo (código, valor, dígito)

        # Para cada Pagamento encontrado
        for codigo, valor, digito in resultado_REGEX:

            # Cria um dicionário para armazenar os dados extraídos
            dadosExtraidos = {}

            # Registra os pagamentos no dicionário
            dadosExtraidos['dtApuracao'] = apuracao
            dadosExtraidos['dtVencimento'] = vencimento
            dadosExtraidos["codigo"] = codigo + "-" + digito
            dadosExtraidos["valor"] = valor

            # Adiciona o dicionário à lista de dados extraídos
            listaResultado.append(dadosExtraidos)

    # Filtra apenas os pagamentos com o código correto
    listaResultadoFiltrada = []
    for pagamento in listaResultado:
        if pagamento["codigo"] in itensCabecalhoFormatado:
            listaResultadoFiltrada.append(pagamento)

    # Se tiverem pagamentos com a mesma data e código, unifica os valores
    pagamentos_unificados = {}

    for pagamento in listaResultadoFiltrada:
        chave = (pagamento["dtApuracao"], pagamento["codigo"])
        if chave not in pagamentos_unificados:
            pagamentos_unificados[chave] = pagamento["valor"]
        else:
            # Os valores estavam como string, então convertemos para float para somar

            # Se for uma String, convertemos para float
            if isinstance(pagamentos_unificados[chave], str):
                pagamentos_unificados[chave] = float(pagamentos_unificados[chave].replace(".", "").replace(',', '.')) # Removendo o ponto e substituindo a vírgula por ponto

            pagamentos_unificados[chave] += float(pagamento["valor"].replace(".", "").replace(',', '.') )# Removendo o ponto, substituindo a vírgula por ponto
            # Após a soma, convertemos de volta para string no formato brasileiro
            pagamentos_unificados[chave] = f"{pagamentos_unificados[chave]:.2f}".replace('.', ',')  # Formata para duas casas decimais e substitui ponto por vírgula


    for (dtApuracao, codigo), valor in pagamentos_unificados.items():
        for row in range(2, ws.max_row + 1):  # Começa em 2 para pular o cabeçalho
            data_celula = ws.cell(row=row, column=1).value
            # Se a célula for datetime, formata para string
            if hasattr(data_celula, 'strftime'):
                data_celula_str = data_celula.strftime("%d/%m/%Y")
            else:
                data_celula_str = str(data_celula)
            if dtApuracao == data_celula_str:
                coluna = itensCabecalhoFormatado.index(codigo) + 2  # +2 para alinhar com o Excel
                ws.cell(row=row, column=coluna, value=valor)

    try:
        # Salva uma cópia da planilha modelo com os dados preenchidos
        wb.save(caminho_pasta_cliente + f"\Sistema S - {cnpj}.xlsx")
    except Exception as e:
        print(f"Erro ao salvar o arquivo: {e}")


if __name__ == "__main__":
    main(
        caminho_planilha_modelo='G:\\Meu Drive\\7. Automação\\OUTRAS AUTOMATIZAÇÕES\\Checklist\\Testes\\Teste Checklist\\Sistema S - SESI SENAI SESC SENAC.xlsx',
        caminho_arquivo='G:\\Meu Drive\\7. Automação\\OUTRAS AUTOMATIZAÇÕES\\Checklist\\Testes\\Teste Checklist\\SEVAN\\Comprovantes de Pagamento.pdf',
        caminho_pasta_cliente='G:\\Meu Drive\\7. Automação\\OUTRAS AUTOMATIZAÇÕES\\Checklist\\Testes\\Teste Checklist\\SEVAN',
        cnpj='39043203000109'
    )
