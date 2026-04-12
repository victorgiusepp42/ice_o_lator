UPLOADER DE IMAGENS — Ice-o-lator / Medusa Arte
===============================================

PASSO A PASSO:

1. PEGAR A CHAVE DA API (gratuita, 1 minuto):
   → Acesse: https://api.imgbb.com/
   → Crie conta ou entre com Google
   → Copie a "API Key" que aparece na tela

2. CONFIGURAR A CHAVE:
   → Abra o arquivo: ferramentas/upload_imagens.py
   → Linha 20: substitua COLE_SUA_CHAVE_AQUI pela sua chave
     API_KEY = "abc123suachaveaqui"

   OU rode assim (sem editar o arquivo):
     IMGBB_KEY=suachave python ferramentas/upload_imagens.py

3. COLOCAR AS IMAGENS:
   → Crie a pasta /imagens/ na raiz do projeto (se não existir)
   → Cole as fotos dos produtos lá dentro
   → Formatos aceitos: JPG, PNG, WEBP, GIF

4. RODAR O SCRIPT:
   → No terminal:  python ferramentas/upload_imagens.py
   → Os links aparecem na tela e são salvos em:
       ferramentas/links_gerados.txt  (prontos para copiar)
       ferramentas/links_gerados.json (formato estruturado)

5. USAR OS LINKS NO SITE:
   → Me manda o arquivo links_gerados.txt aqui no chat
   → Aplico todas as fotos nos cards de uma vez

ESTRUTURA DE PASTAS:
  /imagens/
    tabaqueira-preta.jpg
    tabaqueira-roxa.jpg
    pipe-heat-cooler.jpg
    bong-hello-kitty.jpg
    ...

  /ferramentas/
    upload_imagens.py
    links_gerados.txt   ← gerado após rodar
    links_gerados.json  ← gerado após rodar
