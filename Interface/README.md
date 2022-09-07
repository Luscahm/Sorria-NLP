# Sorria Web Interface

- [Sorria Web Interface](#sorria-web-interface)
  - [Servidor/server](#servidorserver)
    - [Como subir em um servidor](#como-subir-em-um-servidor)
    - [Deploy in a server](#deploy-in-a-server)
  - [Utilizar/Usage](#utilizarusage)
    - [Atualizar Corpus](#atualizar-corpus)
    - [Update corpus](#update-corpus)


---

## Servidor/server
###  Como subir em um servidor
Para conseguir colocar essa interface na internet primeiramente é preciso localizar algum host capaz de suportar aplicações WSGI(Web Server Gateway Interface), pois nossa interface foi criada utilizando a framework Flask, algumas opções são Heruko, Google App engine, Azure, porem qualquer server WSGI suporta essa interface, no [manual do flask em ingles](https://flask.palletsprojects.com/en/2.2.x/deploying/) há algumas opções e alguns tutoriais de como subir nesses servidores. Por cada servidor conter seu próprio método de upload recomenda-se a leitura do manual do mesmo caso queira fazer upload de nossa interface Flask

### Deploy in a server
To deploy this interface on the internet you first need to find a host able to support WSGI applications (Web Server Gateway Interface), because our interface was created using the Flask framework, some options are Heruko, Google App engine and  Azure, but any WSGI server supports this interface, in the [flask manual](https://flask.palletsprojects.com/en/2.2.x/deploying/) there are some options and some tutorials on how to upload to these servers. Because each server contains its own upload method it is recommended to read its manual if you want to upload our Flask interface

## Utilizar/Usage
### Atualizar Corpus
Para atualizar o corpus é ncessario rodar novamente o código presente no Retrieve & Re-rank para poder atualizar as embeddings do corpus e colocar tanto o corpus_embedding.plk quanto o corpus.plk no diretório "data", substituindo a versão anterio.

É necessario realizar esse processo em uma máquina com GPU, ou no Google Colab acelerado por GPU, por se tratar da geração de embedding o mesmo não consegue executar em uma máquina sem GPU
### Update corpus
To update the corpus it is necessary to run the Retrieve & Re-rank code again in order to update the corpus embeddings and put both corpus_embedding.plk and corpus.plk in the "data" directory, replacing the previous version.

This needs to be done on a machine with a GPU, or GPU-accelerated Google Colab, because embedding generation  cannot run on a machine without GPU
