"""GitHub Actions에서 매일 실행되는 원고 자동 생성 스크립트.

app.py의 크롤링 함수를 그대로 재사용해서 output/ 폴더에 .docx를 저장한다.
"""
import os
import time

from docx import Document
from docx.shared import Pt

from app import (
    create_driver,
    get_mbc_anchors_study,
    get_yonhap_shorts_study,
    get_breaking_news_yonhap,
)


def main():
    driver = create_driver()
    try:
        doc = Document()
        for sec in doc.sections:
            sec.top_margin, sec.bottom_margin = Pt(40), Pt(40)
            sec.left_margin, sec.right_margin = Pt(50), Pt(50)

        get_mbc_anchors_study(driver, doc, target_count=3)
        get_yonhap_shorts_study(driver, doc, target_count=7)
        get_breaking_news_yonhap(driver, doc, target_count=5)
    finally:
        driver.quit()

    os.makedirs("output", exist_ok=True)
    path = os.path.join("output", f"Study_Scripts_{time.strftime('%Y%m%d')}.docx")
    doc.save(path)
    print(f"저장 완료: {path}")


if __name__ == "__main__":
    main()
