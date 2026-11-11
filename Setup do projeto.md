# Setup do projeto

**Todas as etapas de preparação da base de dados a ser publicada e criação de usuários deverão estar finalizadas[^1] para realização dos passos descritos a seguir**

## 1- Fork do projeto

1.1 Realize o fork do projeto (utilizaremos um fork para conseguir atualizar as automatizações com maior facilidade no futuro):
 
  - Clique em Fork e em seguida "Create a new fork"

![fork_projeto](https://imgur.com/uOZlh8a.png)

1.2 Selecione a organização a qual o novo conjunto de dados será criado e preencha o nome do novo repositório (**o nome deverá ser o mesmo do conjunto que será criado na instância do CKAN**).

 OBS.: Certifique-se que o nome desejado para o novo conjunto não está sendo usando, pela lista dos conjuntos atualmente publicados [em ambiente de produção](https://dados.mg.gov.br/api/3/action/package_list) e [homologação](https://homologa.cge.mg.gov.br/api/3/action/package_list) ou pelas respectivas páginas dos conjuntos publicados: [produção](https://dados.mg.gov.br/dataset/) e [homologação](https://homologa.cge.mg.gov.br/dataset/)

![fork_org_name](https://imgur.com/bqSjsyQ.png)

## 2- Cadastro das Secrets

Para publicação no Portal de Dados Abertos deverão ser criadas três secrets: 

  - OWNER_ORG: Elaborada pela Diretoria de Transparência Ativa/CGE como parte do processo de criação do repositório;\
  - CKAN_HOST: Elaborada pela Diretoria de Transparência Ativa/CGE como parte do processo de criação do repositório;\
  - **CKAN_KEY_USUARIOGITHUB: Gerada pelo servidor responsável pela disponibilização dos dados.**


### 2.1 Cadastrar a secrets para publicação em instância CKAN 

- Clique em Settings > Secrets and variables > New repository secret 

![fork_settings](https://imgur.com/I3OFQwu.png)-------------------------

![fork_secrets](https://imgur.com/aan0HNd.png)--------------------------

![fork_new_secrets](https://imgur.com/Xg2TLCd.png)

### 2.2 Criação das secrets:

#### 2.2.1  OWNER_ORG 
Organização dentro da instância do CKAN desejada a qual o conjunto de dados será vinculado (nome disponível na url CKAN após `https://ckan-instance/organization/`).<br>

Exemplos:
  - `controladoria-geral-do-estado-cge` em https://dados.mg.gov.br/organization/controladoria-geral-do-estado-cge
  - `secretaria-de-estado-de-planejamento-e-gestao-seplag` em https://homologa.cge.mg.gov.br/organization/secretaria-de-estado-de-planejamento-e-gestao-seplag.


#### 2.2.2 CKAN_HOST 
Local onde os dados serão publicados, ou seja, ambiente de homologação (teste) ou ambiente de produção.

Exemplo: Instância CKAN desejada:`https://homologa.cge.mg.gov.br`

#### 2.2.3 CKAN_KEY_USUARIOGITHUB

É importante certificar-se o usuário está cadastrado para a organização que deseja cadastrar o novo conjunto de dados, seja em [produção](https://dados.mg.gov.br/dashboard/organizations) em [homologação](https://homologa.cge.mg.gov.br/dashboard/organizations)

Exemplo: Se meu usuário GitHub é `gabrielbdornas` este secret será `CKAN_KEY_GABRIELBDORNAS`. Para o `andrelamor`, o secret `CKAN_KEY_ANDRELAMOR`

Para completar o cadastro na instância CKAN_KEY é necessário criar um novo API Token (copiar e colar o valor `API TOKEN created`) na instância que será realizada a publicação:

![ckan_chave](https://imgur.com/Dr1VxG8.png)
------------------------------------------

![ckan_chave_token](https://imgur.com/TpUQoLM.png)
------------------------------------------

![ckan_chave_nome](https://imgur.com/AwD8hgc.png)
------------------------------------------

  - Copiar e colar esse valores `API TOKEN created`

![ckan_chave_criada](https://imgur.com/4qgD7HS.png)



## 3 - Configurar permissão para Actions ler e escrever no repositório

Caso a permissão para Actions ler e escrever no repositório não esteja habilitada, esta configuração deverá ser feita também no nível da organização.

![fork_settings](https://imgur.com/I3OFQwu.png)

![image](https://github.com/transparencia-mg/new-dataset-template/assets/49699290/7e5f739a-1b15-4bd1-a225-1cd75655d80b)

## 4- ACTIONS

Após finalizar os passos acima, clicar em Actions e selecionar o botão verde " I understand my workflows, go ahead and enable them"

![image](https://github.com/user-attachments/assets/8be5b36d-4404-4409-8bdc-ef823c43641e)


## 5- Publicação dos arquivos

### 5.1 Inclusão

Para rodar o processo automatizado é necessária a inclusão do arquivo .xlsx ou .xls na pasta de dados `upload` do novo repositório forkado e configurado.

![image](https://github.com/transparencia-mg/new-dataset-template/assets/53793354/8c6b1794-88e4-41c8-97c6-9fa751bce23f)

Após incluir o arquivo o processo encontra-se concluído. Verifique se os dados foram corretamente publicados

### 5.1 Atualização dos arquivos publicados

5.1.1 Para alterar/atualizar os arquivo: README, CHANGELOG, CONTRIBUTING e DATAPACKEGE.yaml referente aos dados publicados é **necessário estar dentro da pasta `dataset`;**

**ATENÇÃO: NÃO ALTERAR/EDITAR DATAPACKEGE.json, apenas mexer no DATAPACKEGE.yaml.**

5.1.2 Para alterar/atualizar  os arquivos excel (xlsx ou xls) clicar na pasta upload. Importante destacar que os arquivos devem ter sempre o mesmo nome para que a atualização ocorra de forma eficaz.

As modificações automáticas só serão publicadas no CKAN se as alterações forem realizadas nestas pastas. 

**ATENÇÃO: NÃO ALTERAR/EDITAR os arquivos da raiz do template.**:

![image](https://github.com/transparencia-mg/new-dataset-template/assets/52294411/3e0dd4fa-cd29-420e-b9b7-1b1c888802e5)

## 6- Atualizações de dados

### 6.1 A partir do repositório template

- Nos repositórios forkados do new-dataset-template, observar se há commits do repositório template para serem sincronizados:

![image](https://github.com/transparencia-mg/new-dataset-template/assets/52294411/060715a7-e1e1-43a3-9a76-9286f20b4807)


2- Caso positivo, clique em `Sync fork`e, depois, no botão `update branch`:
![image](https://github.com/transparencia-mg/new-dataset-template/assets/52294411/82642ae9-7d97-4e84-9603-6701e4591cb6)

3- Aparecerá a mensagem na tarja superior em azul-claro:

![image](https://github.com/transparencia-mg/new-dataset-template/assets/52294411/5a259c7e-61ab-42cc-ae0e-dadce259778e)

Observe que o repositório clonado na máquina precisará do `pull`, para ser atualizado após esse sync, como qualquer alteração que ocorre no github.

**Observação:**

Clicando em `Fork`, é possível listar todos os repositórios que foram gerados a partir do new-dataset-template, e conferir um por um:

![image](https://github.com/transparencia-mg/new-dataset-template/assets/52294411/55a59bac-d1b4-4383-ad0d-cb5dcfc5ac3d)

#### Arquivo excel com mais de uma aba

Abas: caso mais de uma aba em um arquivo excel necessite ser convertida para CSV, basta descomentar o código no arquivo `config.py` e incluir o nome do arquivo (com a correta extensão) e sua(s) respectiva(s) aba(s) para conversão.
````
abas = {
#     'nome_do_arquivo.xlsx': [
#         'nome_da_aba1',
#         'nome_da_aba2',
#         'nome_da_aba3',
#     ],
````

## 7- Inclusão e exclusão de arquivos

### 7.1 Incluir um arquivo novo

Coloque o novo Excel na pasta `upload` (ou o CSV direto em `dataset/data`). Vale para qualquer arquivo: novo ano, nova aba, nova tabela. A automação converte o Excel em CSV, inclui o recurso no `datapackage.yaml` e o cria no CKAN. O recurso novo aproveita a documentação de um recurso que já existe:

- **mesma série no nome** (só números diferentes, ex.: `estagiarios_2026` → `estagiarios_2027`, `folha_2026_01` → `folha_2026_02`): copia título e descrição trocando os números;
- **mesmas colunas** de um recurso existente: copia o schema, com tipos e descrições das colunas;
- **colunas diferentes** do recurso da série: o schema é inferido do CSV novo, mantendo a documentação das colunas que continuaram, e o log mostra `REVISAR`;
- **nenhuma semelhança**: título e descrição entram para preencher.

**Depois da publicação, revise no `datapackage.yaml` o título e a descrição do recurso novo.**

### 7.2 Excluir um arquivo

Apague o Excel da pasta `upload` (ou retire a aba do `config.py`). A automação apaga o CSV correspondente em `dataset/data`, retira o recurso do `datapackage.yaml` e do `datapackage.json` e exclui o recurso no CKAN. Para CSVs colocados direto em `dataset/data`, basta apagar o CSV.

**Atenção:** apagar o Excel do `upload` exclui o recurso publicado. Não apague arquivos do `upload` só para "limpar" a pasta. Se precisar desligar a exclusão automática de CSVs em um repositório, inclua `remover_excluidos = False` no `scripts/config.py`.

Por segurança, se `dataset/data` ficar sem nenhum CSV, nada é excluído. A automação só exclui no CKAN recursos que ela mesma criou; recursos incluídos à mão no CKAN não são tocados.

[^1]: [Ciclo de Abertura, Documentação, Validação e Publicação](https://transparencia-mg.github.io/manual-dados-mg/0.1/2.%20Ciclo%20de%20publica%C3%A7%C3%A3o%20de%20dados/006_etapas_abertura/).
