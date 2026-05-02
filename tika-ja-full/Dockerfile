FROM apache/tika:3.3.0.0-full

USER root

# Add practical utilities for Japanese OCR pipelines
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      ocrmypdf \
      tesseract-ocr-jpn \
      tesseract-ocr-jpn-vert \
      tesseract-ocr-osd \
      ghostscript \
      imagemagick \
      qpdf \
      poppler-utils \
      poppler-data \
      libreoffice \
      libreoffice-l10n-ja \
      libreoffice-help-ja \
      fonts-noto-cjk \
      fonts-ipaexfont \
      fonts-ipafont-gothic \
      fonts-ipafont-mincho \
      locales \
    && rm -rf /var/lib/apt/lists/*

RUN locale-gen ja_JP.UTF-8 && update-locale LANG=ja_JP.UTF-8

ENV LANG=ja_JP.UTF-8
ENV LC_ALL=ja_JP.UTF-8

# Keep the same non-root user policy as the base image typically uses
USER 1000
