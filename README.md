# Instalar dependências
npm install

# Build do projeto
npm run build

# Publicar no npm
npm publish


características do Pacote:
Performance: Usa sendBeacon para envio assíncrono

Privacidade: Filtro de dados sensíveis via beforeSend

Flexibilidade: Configuração extensível e hooks personalizados

Type Safety: Tipos TypeScript completos

Sample Rate: Controle de volume de dados

Ignorar elementos: Selectors personalizáveis

Debug: Modo de desenvolvimento com logs

Este pacote fornece uma solução completa e profissional para monitoramento de cliques em produção.

----

# Listar versões disponíveis
nvm list available

# Instalar uma versão específica
nvm install 18.17.0

# Usar uma versão específica
nvm use 18.17.0

# Criar arquivo .nvmrc com a versão
echo "18.17.0" > .nvmrc

# Usar a versão do .nvmrc
nvm use

#### get token influxdb3

influxdb3 create token --admin

influxdb3 create token --admin --regenerate 


Bearer apiv3_tTs0gaStoeMCBm_R1JuvAXYglv3k-LpNeF5CaTSRKWWnZIMlZThADb5n2HxvJQE5H9ijcsVIoHbtRUvqKvGCAA

#### Criar database usando o CLI
nfluxdb3 create database <database> --token <token>

#### Links

https://page-speed.dev/www.google.com
https://github.com/danielroe/page-speed.dev


#### QUERIES

```SQL

  select page_url, count(time) as total from 'click_event' WHERE time >= now() - interval '5 minutes'  GROUP by page_url order by total desc


  select page_url, click_text, count(time) as total from 'click_event' WHERE time >= now() - interval '5 minutes'  GROUP by page_url, click_text order by total desc

   SELECT distinct page_url, name, count FROM web_vitals WHERE time >= now() - interval '5 minutes' order by  page_url, name

```