# Consulta Processual - TJRJ

Este projeto consulta informações de um processo judicial no site do Tribunal de Justiça do Rio de Janeiro (TJRJ), a partir do número do processo.

## Como usar

Faça uma requisição POST para `/consultar` com um JSON contendo:

```json
{
  "numero_processo": "0800620-36.2021.8.19.0002"
}
