# Excel Essentials: Fórmulas para Analistas

**🔍 BUSCA & REFERÊNCIA**
```excel
=PROCX()          # Busca simples
=ÍNDICE+CORRESP() # Busca avançada qualquer direção
=FILTRO()         # Retorna múltiplas linhas
```

---

**🧹 LIMPEZA DE DADOS**
```excel
=ARRUMAR(A1)        # Remove espaços extras
=MAIÚSCULA(A1)      # Tudo maiúsculo
=MINÚSCULA(A1)      # Tudo minúsculo
=PRI.MAIÚSCULA(A1)  # Primeira letra maiúscula
=TIRAR(A1)          # Remove caracteres invisíveis
=VALOR(A1)          # Converte texto em número
=TEXTO(A1;"00000")  # Número em texto formatado
```

---

**🔗 TEXTO**
```excel
=CONCAT(A1;" ";B1)        # Une células
=EXT.TEXTO(A1;1;5)        # Extrai parte do texto
=LOCALIZAR("@";A1)        # Acha posição de caractere
=SUBSTITUIR(A1;"SP";"RJ") # Substitui texto
=NÚM.CARACT(A1)           # Conta caracteres
```

---

**📊 CÁLCULO CONDICIONAL**
```excel
=SOMASE(C:C;"SP";D:D)          # Soma com 1 condição
=SOMASES(D:D;C:C;"SP";B:B;">5")# Soma com várias condições
=CONT.SE(C:C;"SP")             # Conta com 1 condição
=CONT.SES()                    # Conta com várias condições
=MÉDIASE()                     # Média com condição
```

---

**🛡️ TRATAMENTO DE ERRO**
```excel
=SEERRO(fórmula;"erro")   # Se der erro, mostra texto
=SENÃODISP(fórmula;"—")   # Específico pro erro #N/A
=ÉERROS(A1)               # Retorna VERDADEIRO se erro
=ÉCÉL.VAZIA(A1)           # Verifica célula vazia
```

---

**📅 DATA**
```excel
=HOJE()                    # Data atual
=AGORA()                   # Data e hora atual
=DATEDIF(A1;B1;"D")        # Diferença em dias
=DATEDIF(A1;B1;"M")        # Diferença em meses
=DIA.DA.SEMANA(A1;2)       # Dia da semana
=FIMMÊS(A1;0)              # Último dia do mês
=TEXTO(A1;"MMMM/AAAA")     # Formata data em texto
```

---

**🔢 ESTATÍSTICA RÁPIDA**
```excel
=MÁXIMO(A:A)       # Maior valor
=MÍNIMO(A:A)       # Menor valor
=MÉDIA(A:A)        # Média
=MED(A:A)          # Mediana
=MODO.ÚNICO(A:A)   # Valor mais frequente
=QUARTIL(A:A;1)    # Quartil
=DESVPAD(A:A)      # Desvio padrão
```

---

**💡 As 20% que resolvem 80% dos problemas no dia a dia:**

| Prioridade | Fórmula |
|---|---|
| ⭐⭐⭐ | PROCX, ÍNDICE+CORRESP, FILTRO |
| ⭐⭐⭐ | SOMASES, CONT.SES, MÉDIASE |
| ⭐⭐⭐ | SEERRO, ARRUMAR, VALOR |
| ⭐⭐ | CONCAT, SUBSTITUIR, TEXTO |
| ⭐⭐ | HOJE, DATEDIF, FIMMÊS |