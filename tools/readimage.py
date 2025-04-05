# Databricks notebook source
import base64
import mimetypes
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def download_image_as_data_url(image_url: str) -> str:
    response = requests.get(image_url)
    if response.status_code != 200:
        raise ValueError(f"下载失败，状态码: {response.status_code}")

    mime_type = response.headers.get('Content-Type')
    if not mime_type:
        mime_type, _ = mimetypes.guess_type(image_url)

    if not mime_type or not mime_type.startswith("image/"):
        raise ValueError(f"返回内容不是图片类型，而是: {mime_type}")

    base64_data = base64.b64encode(response.content).decode('utf-8')
    return f'data:{mime_type};base64,{base64_data}'

def extract_first_image_url_from_html(html_content: str, base_url: str) -> str:
    soup = BeautifulSoup(html_content, 'html.parser')
    img_tag = soup.find('img')
    if not img_tag or not img_tag.get('src'):
        raise ValueError("未在 HTML 中找到图片标签 <img>")

    return urljoin(base_url, img_tag['src'])

def readimage(image_url: str) -> dict:
    response = requests.get(image_url)
    if response.status_code != 200:
        raise ValueError(f"下载失败，状态码: {response.status_code}")

    content_type = response.headers.get('Content-Type', '')

    if content_type.startswith('text/html'):
        extracted_image_url = extract_first_image_url_from_html(response.text, image_url)
        data_url = download_image_as_data_url(extracted_image_url)
        return {
            'from_html': True,
            'original_url': image_url,
            'extracted_image_url': extracted_image_url,
            'result': data_url
        }

    data_url = download_image_as_data_url(image_url)
    return {
        'from_html': False,
        'original_url': image_url,
        'extracted_image_url': '',
        'result': data_url
    }

# ✅ 加入 main 函数用于测试
if __name__ == "__main__":
    # 你可以替换成任意 HTML 页面或图片的 URL
    test_url = "http://jp.highwayns.com/wp/wp-content/themes/biz-vektor/images/headers/bussines_desk_01.jpg"  # HTML 页面中包含 logo 图片
    try:
        result = readimage(test_url)
        print("\n=== 图片处理结果 ===")
        print("是否来自 HTML 页面:", result['from_html'])
        print("原始链接:", result.get('original_url') or result.get('image_url'))
        print("图片链接:", result.get('extracted_image_url', result.get('image_url')))
        print("图片 Data URL (前200字符):", result['result'][:200], "...")
    except Exception as e:
        print("发生错误:", e)
