# Refactor 04 — robustez dos relatórios

## Objetivo

Centralizar a conversão de DOCX para PDF e tornar explícitos os diferentes resultados possíveis, sem transformar a ausência do LibreOffice em falha fatal do pipeline.

## Decisões

- `src/relatorios/conversao_pdf.py` concentra localização e execução do LibreOffice.
- `ResultadoConversaoPDF` registra sucesso, caminho, código de retorno, mensagem e `stderr`.
- `ResultadoRelatorio` preserva as chaves legadas `docx`, `markdown` e `pdf`, acrescentando `conversao_pdf`.
- Matemática e Física passam a usar o mesmo contrato.
- DOCX e Markdown continuam válidos quando a conversão não pode ser executada.
- O relatório regional de Física não foi alterado porque atualmente não solicita conversão automática para PDF.

## Limite desta etapa

A geração textual completa ainda permanece nos módulos específicos. A decomposição entre carga, tabelas, texto e renderização será aplicada desde Letras–Inglês e migrada para os relatórios anteriores apenas mediante teste de regressão documental.

## Validação

```powershell
python executar_refactor_04.py
pytest -q -m "not integration"
pytest -q -m integration
pytest -q
ruff check .
```
