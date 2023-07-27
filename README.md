## Disclosure of job offers API - Divulgação de vagas de empregos

API desenvolvida para armazenamento e controle dos dados das demais aplicações desenvolvidas.

Esse projeto funciona juntamente com outras três aplicações:


- [Disclosure of job offers](https://github.com/ZzZzNeto/NewDVE-Front)
- [Manager Employees](https://github.com/ZBreno/ManagerFront)
- [Manager Employees API](https://github.com/ZBreno/ManagerBack) 


Projeto desenvolvido na disciplina de Desenvolvimento de Projetos II, utilizando os conhecimentos adquiridos nas demais, como Administração de Banco de Dados, Processo de Software, Arquitetura de Software e Desenvolvimento de Sistemas Distribuídos.

## Desenvolvedores

Jose Neto & [Breno Soares](https://github.com/ZBreno)

## Documentações

- [📄 Requisitos funcionais/não funcionais](https://docs.google.com/document/d/1FlwLnmnZ4Tu4Oay_JIqlUjqPI2i-paz1/edit?usp=sharing&rtpof=true&sd=true)
- [👩🏻‍💻 Casos de uso](https://drive.google.com/file/d/1CJjRd100EArTfbCyiPwp05XBsz39KLBj/view?usp=sharing)
- [🔗 Diagrama de classes](https://drive.google.com/file/d/10Cvp5g0iA7wh9mp8YT4DNKgFFdNFLGVE/view?usp=sharing)
- [⚙️ Visão funcional](https://drive.google.com/file/d/1zk8mlfRKxi3XWtymagDZsFrYu00zn3k4/view?usp=sharing)
- [🔌 Visão de implantação](https://drive.google.com/file/d/1pCJbjAPXYd5qoU0b3weIGGMbw0FlXBYo/view?usp=sharing)
- [🛠️ Visão de desenvolvimento](https://drive.google.com/file/d/13wACc3RVuCWbo2AcGxxE_epxcBvMyXsM/view?usp=sharing)
- [📚 C4 Context](https://drive.google.com/file/d/1Mmw3xXB5UuM2uamh5AEEI0ClS5SJEw6-/view?usp=sharing)
- [📚 C4 Container](https://drive.google.com/file/d/1A_eV3jdoTnW7kOGnlzwG3rGNoCXsgMWI/view?usp=sharing)
- [📚 C4 Components](https://drive.google.com/file/d/1Ut9Ell6q5DgQx9vCx_sfVuSQrOmEl926/view?usp=sharing)
- [🖌️ Protótipo da interface (figma)](https://www.figma.com/file/8XTGRhLe3SwlVz2RbYbqpE/Disclosure-of-job-offers-%26-Manager-Employees?type=design&node-id=0%3A1&mode=design&t=T39YGZbkLURcNLms-1)


## Tecnologias utilizadas

- Django Rest Framework

## Instalação

Após clonar o repositório e criar um ambiente virtual, basta executar o comando abaixo para instalar as dependências do projeto.

```bash
pip install -r requirements.txt
```

Primeiro, é preciso configurar seu banco de dados criando um arquivo `.env` na pasta `config` do projeto.
Logo após, execute este comando para rodar as migrações no banco e gerar as tabelas.
```bash
py manage.py migrate
```

Por fim, para rodar o projeto, basta usar o comando a seguir
```bash
py manage.py runserver
```

Após instalar, basta rodar com o comando a seguir para executar o projeto
```bash
npm run dev
# or
yarn dev
```
Após isso acesse [http://seuip:8000/](http://127.0.0.1:8000)
