# Site BTech Consultoria

Landing page institucional estática para a **BTech Consultoria**, criada com HTML, CSS e JavaScript puro.

A proposta visual segue o manual de identidade enviado: uso de colmeia, tipografia com referência à Century Gothic, paleta reduzida da marca e uma comunicação consultiva, humana e operacional.

O conceito central do site é **proximidade operacional**: tecnologia forte sem perder humanidade, com clareza, acompanhamento e construção conjunta.

## Estrutura

- `index.html`: landing única com hero, ideia central, quem somos, pessoas, como ajudamos, forma de trabalho, cloud acompanhada, IA e automação, onde atuamos, FAQ e contato.
- `cloud.html`: redireciona para `index.html#cloud-acompanhada`.
- `styles.css`: sistema visual, responsividade, componentes e aplicação da identidade ABTech.
- `script.js`: menu mobile, ano automático e feedback do formulário.
- `assets/source/manual-abtech.pdf`: manual de marca ABTECH — fonte do símbolo e da tipografia.
- `scripts/build-logos.py`: gera BTECH (remove só o «A»; mantém símbolo, cores e «TECH» do manual).
- `assets/logo-btech-stacked-oficial.png` / `logo-btech-horizontal-oficial.png`: lockups oficiais para o site.
- `assets/visuals/`: padrões e painéis com colmeia/hexágonos conforme o manual.

## Como abrir localmente

Abra `index.html` no navegador ou rode um servidor local:

```bash
python3 -m http.server 8000
```

Depois acesse `http://localhost:8000`.

## Próximos ajustes recomendados

1. Substituir o SVG temporário pelo logotipo oficial em arquivo vetorial, se disponível.
2. Conectar o formulário de contato a um serviço de envio.
3. Inserir clientes, segmentos, cases e logos conforme a ABTech consolidar esses materiais.
4. Revisar textos finais com os responsáveis Erico e Alexandre antes da publicação.
