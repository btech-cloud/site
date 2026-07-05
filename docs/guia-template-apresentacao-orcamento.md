# Guia — Template de apresentação e orçamento BTech

Formato **1920×1080 (16:9)** · Identidade visual alinhada aos posts Instagram (hexágonos, teia de conexões, gradientes, luz humana + tecnologia).

## Arquivos

| Arquivo | Uso |
|---------|-----|
| `assets/presentations/btech-template-orcamento.pptx` | Template pronto para editar |
| `assets/presentations/template/bg-dark-network.png` | Fundo escuro (capa, investimento, fechamento) |
| `assets/presentations/template/bg-light-network.png` | Fundo claro (texto, tabelas, fotos) |
| `scripts/presentation_theme.py` | Paleta, fundos gerados, helpers visuais |
| `scripts/build-orcamento-template.py` | Regenera o PPTX após mudanças de layout |

### Regenerar o template

```bash
cd scripts
python3 build-orcamento-template.py
```

Dependências: `python-pptx`, `Pillow`.

---

## Slides incluídos (18)

1. **Guia do template** — excluir antes de enviar ao cliente  
2. **Capa** — título, cliente, referência  
3. **Sumário** — agenda da proposta  
4. **Quem somos** — posicionamento + foto equipe  
5. **Por que B** — Bridge, Build, Beta, Brasil, Better, Backup  
6. **Contexto** — cenário do cliente + números em destaque  
7. **Desafios** — lista numerada (fundo escuro)  
8. **Objetivos** — bullets + foto workshop  
9. **Visão da solução** — statement principal  
10. **Arquitetura / fluxo** — hexágonos conectados (pesos de linha variáveis)  
11. **Escopo** — tabela editável  
12. **Cronograma** — fases em faixas  
13. **Entregáveis** — tabela por fase  
14. **Investimento** — tabela + recorrência opcional  
15. **Condições** — premissas e exclusões (duas colunas)  
16. **Por que BTech** — 4 diferenciais + credenciais  
17. **Próximos passos** — fluxo em 4 etapas  
18. **Encerramento** — frase de marca + contato  

---

## Identidade visual aplicada

### Paleta
- Violeta `#6E1EE6` · Azul `#143CFF` · Ciano `#00E1B4` / `#00FFFF`  
- Magenta `#C800D2` · Âmbar `#FFAF3C`  
- Fundo escuro `#050510` → `#1A0B40`  
- Fundo claro `#FAFBFF`

### Elementos
- **Hexágonos** — cheios, contornos e brilhos desfocados (como nos posts)  
- **Teia de conexões** — linhas com espessuras diferentes (junções mais fortes = integrações críticas)  
- **Orbs / bokeh** — luz ambiente, não datacenter  
- **Fotos** — pessoas em contexto corporativo (equipe, workshop, conversa com cliente)  
- **Barra gradiente** — violeta → azul → ciano → âmbar (rodapé dos heroes)  
- **Logo** — horizontal (claro/escuro conforme fundo)

### Tom de conteúdo
- Pragmático e comercial (orçamento que converte)  
- Posicionamento de **ampliação de capacidade** (não manifesto)  
- Termos técnicos quando agregam credibilidade (multicloud, DR, LLMs, CI/CD)  
- **B** como alternativa com significado (Bridge, Build, Beta, Brasil…)

---

## Como adaptar para cada orçamento

1. **Exclua** o slide "Guia do template".  
2. **Capa** — preencha `[Nome da empresa]`, referência e data.  
3. **Contexto / Desafios** — troque números e bullets pelo diagnóstico real.  
4. **Arquitetura** — renomeie nós para sistemas do cliente (ERP, CRM, AWS, etc.).  
5. **Escopo / Entregáveis / Investimento** — ajuste linhas e valores.  
6. **Condições** — alinhe com jurídico/financeiro (pagamento, validade).  
7. Duplique ou remova slides conforme o tamanho da proposta (MSP pode precisar mais de parceria; cliente final, mais de escopo técnico).

---

## Onde usar o mesmo template

- Propostas comerciais e orçamentos  
- Apresentações para integradores / MSPs  
- Kick-off de projeto (reutilizar arquitetura + cronograma)  
- Decks internos de validação (Bruno, fundadores) — trocar textos, manter visual  

---

## Referências que faltam (opcional)

Se você enviar os posts Instagram originais ou o deck Binário em arquivo, podemos:
- Calibrar opacidade dos hexágonos 1:1 com os posts  
- Adicionar slides específicos do modelo Binário (SLA, matriz RACI, diagrama de rede)  
- Incluir master slides no PowerPoint (Layouts reutilizáveis em vez de slides duplicados)

---

## Contato no template

comercial@b-tech.cloud · (11) 9 3022-6495 · btech.cloud
