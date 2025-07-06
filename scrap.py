from flask import Flask, request, jsonify, send_file
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options       
import time
import requests
import os
from fpdf import FPDF
from PIL import Image
import io

app = Flask(__name__)

# salvar as imagens dos capítulos

IMAGES_PATH = 'imagens'
os.makedirs(IMAGES_PATH, exist_ok=True)

@app.route('/baixar_manga/<nome>/<capitulo>', methods=['POST'])
def baixar_manga(nome, capitulo):
    url = f'https://mangalivre.tv/manga/{nome}/capitulo-{capitulo}/'

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=chrome_options)

    imagens_baixadas = []

    try:
        driver.get(url)
        time.sleep(3)  

        div = driver.find_element(By.CLASS_NAME, 'chapter-images')
        imagens = div.find_elements(By.TAG_NAME, 'img')

        for index, img in enumerate(imagens):
            src = img.get_attribute('src')
            if src:
                try:
                    response = requests.get(src)
                    if response.status_code == 200:
                        try:
                            image = Image.open(io.BytesIO(response.content))
                            img_path = os.path.join(IMAGES_PATH, f'imagem_{index}.jpg')
                            image.save(img_path, 'JPEG')
                            imagens_baixadas.append(img_path)
                            print(f'imagem {index + 1} baixada com sucesso.')
                        except Exception as e:
                            print(f'erro ao processar a imagem {index + 1}: {e}')
                except Exception as e:
                    print(f'erro ao baixar imagem {index + 1}: {e}')

        # cria o pdf
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=10)

        for img_path in imagens_baixadas:
            pdf.add_page()
            pdf.image(img_path, x=10, y=10, w=190)

        # salva o pdf
        pdf_path = f'{nome}_capitulo_{capitulo}.pdf'
        pdf.output(pdf_path)

        return send_file(pdf_path, as_attachment=True, download_name=pdf_path)

    finally:
        driver.quit()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
