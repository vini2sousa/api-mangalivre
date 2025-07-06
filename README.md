# api-mangalivre
API para automação do download de capítulos de mangá do site MangaLivre (https://mangalivre.tv).  
Desenvolvida com **Flask** e **Selenium**, a aplicação acessa a página do capítulo desejado, baixa as imagens e gera um arquivo PDF para leitura offline.

## Tecnologias usadas

- Flask (microframework web)
- Selenium (automatização do navegador)
- Docker (Conteinerização)
- webdriver-manager (gerenciamento do ChromeDriver)
- requests (download das imagens)
- Pillow (manipulação de imagens)
- FPDF (geração do arquivo PDF)

## Como usar

Construa a Imagem
No diretório do projeto (onde está o `Dockerfile`), execute:
```bash
docker build -t api-mangalivre .
````

Rode o Container
```bash
docker run -p 5000:5000 api-mangalivre 
````
Utilize o método POST no endpoint
  ```bash
  http://localhost:5000/baixar_manga/<nome-do_manga>/<numero-do-capitulo>
  ````
Exemplo prático com httpie
```bash
http POST http://localhost:5000/baixar_manga/one-piece/10
```
## Observações
- As imagens são capturadas e alocadas na pasta "Imagens".
- Uma versão em PDF será gerada no diretório principal da aplicação.
- Caso o mangá tenha espaço no nome, utilizar "-", Ex: One-piece.
