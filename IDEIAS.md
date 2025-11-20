# Idéias

## Desenho

 - Criar desenho do fluxo da solução
 - criar fluxograma do agent 

## Features
 
### RUM AGENT 
 - Não zerar o buffer de envio quando falhar o envio para o coletor
 - Opção para gerar data na coleta do agents
 - Tempo de tela
 - metricas de agentes
 
### Coletor
 - Criar configuração para optar pela data do coletor ou do agent 
 - fazer o flush sumarizado para diminuir a granularidade, entender se é melhor fazer no coletor ou no agente
 - Quebrar o user_agent para constabilizar os diferentes tipos de agentes

### Dash / Painel
  - Sessoes engajadas
  - UTM
  | Parameter |	Description |
  |  utm_campaign |	Identifies the campaign. |
  |  utm_medium	| Identifies the medium, such as a search engine, a social media platform, or another platform. |
  |  utm_source	 | Identifies the source of the traffic, such as Google or AdWords. |
  |  utm_term |	Identifies keywords that generate clicks. |
  |  utm_content | Identifies the content zone, such as a call-to-action message. |

    ?utm_source=google&utm_medium=cpc &utm_campaign=AwesomeAdWordsCampaign&gclid=CKSDxc_qhLkCFQyk4AodO24Arg

    Pegar via webvital FCP