"use strict";

const { Plugin } = require("obsidian");

// 与 pictrue_optimize.css 中的排除项保持一致：标注、缩略图、社区截图、画布图片不参与放大
const EXCLUDE_SELECTOR =
  ".callout-content img, .thumbnailImage, .community-item-screenshot, .canvas img";

const MIN_SCALE = 0.2;
const MAX_SCALE = 20;
const STEP = 1.1;
const DRAG_THRESHOLD = 4; // 小于该位移视为单击（关闭），否则视为拖动（平移）

module.exports = class ImageClickZoom extends Plugin {
  onload() {
    this.overlay = null;
    this.img = null;
    this.scale = 1;
    this.tx = 0;
    this.ty = 0;

    this.dragging = false;
    this.moved = false;
    this.startX = 0;
    this.startY = 0;
    this.baseTx = 0;
    this.baseTy = 0;

    // 双击：未放大时打开放大层。捕获阶段拦截，避免触发 Obsidian 自身行为
    this.registerDomEvent(
      document,
      "dblclick",
      (evt) => {
        if (this.overlay) return;
        const target = evt.target;
        if (!(target instanceof HTMLImageElement)) return;
        if (target.matches(EXCLUDE_SELECTOR)) return;
        if (target.closest(".callout, .canvas")) return;
        if (!target.currentSrc && !target.src) return;
        this.open(target.currentSrc || target.src);
        evt.preventDefault();
        evt.stopPropagation();
      },
      { capture: true }
    );

    // 单击放大层：关闭（除非刚刚发生过拖动）
    this.registerDomEvent(
      document,
      "click",
      (evt) => {
        if (!this.overlay) return;
        if (this.moved) {
          this.moved = false;
          return;
        }
        this.close();
        evt.preventDefault();
        evt.stopPropagation();
      },
      { capture: true }
    );

    // Ctrl + 滚轮：在放大状态下继续缩放
    this.registerDomEvent(
      document,
      "wheel",
      (evt) => {
        if (!this.overlay || !evt.ctrlKey) return;
        evt.preventDefault();
        const factor = evt.deltaY < 0 ? STEP : 1 / STEP;
        this.scale = Math.min(Math.max(this.scale * factor, MIN_SCALE), MAX_SCALE);
        this.apply();
      },
      { capture: true, passive: false }
    );

    // 拖动平移
    this.registerDomEvent(document, "mousedown", (evt) => {
      if (!this.overlay || evt.button !== 0) return;
      this.dragging = true;
      this.moved = false;
      this.startX = evt.clientX;
      this.startY = evt.clientY;
      this.baseTx = this.tx;
      this.baseTy = this.ty;
      this.overlay.classList.add("icz-grabbing");
      evt.preventDefault();
    });

    this.registerDomEvent(document, "mousemove", (evt) => {
      if (!this.dragging) return;
      const dx = evt.clientX - this.startX;
      const dy = evt.clientY - this.startY;
      if (Math.abs(dx) > DRAG_THRESHOLD || Math.abs(dy) > DRAG_THRESHOLD) {
        this.moved = true;
      }
      this.tx = this.baseTx + dx;
      this.ty = this.baseTy + dy;
      this.apply();
    });

    this.registerDomEvent(document, "mouseup", () => {
      if (!this.dragging) return;
      this.dragging = false;
      if (this.overlay) this.overlay.classList.remove("icz-grabbing");
    });

    // Esc 关闭
    this.registerDomEvent(document, "keydown", (evt) => {
      if (evt.key === "Escape" && this.overlay) {
        this.close();
        evt.preventDefault();
      }
    });
  }

  open(src) {
    this.scale = 1;
    this.tx = 0;
    this.ty = 0;

    const overlay = document.createElement("div");
    overlay.className = "icz-overlay";

    const img = document.createElement("img");
    img.className = "icz-img";
    img.src = src;
    overlay.appendChild(img);

    document.body.appendChild(overlay);
    this.overlay = overlay;
    this.img = img;

    // 下一帧再加 visible，触发淡入过渡
    window.requestAnimationFrame(() => overlay.classList.add("icz-visible"));
    this.apply();
  }

  apply() {
    if (this.img) {
      this.img.style.transform = `translate(${this.tx}px, ${this.ty}px) scale(${this.scale})`;
    }
  }

  close() {
    if (!this.overlay) return;
    const overlay = this.overlay;
    this.overlay = null;
    this.img = null;
    this.scale = 1;
    this.tx = 0;
    this.ty = 0;
    this.dragging = false;
    this.moved = false;
    overlay.classList.remove("icz-visible");
    window.setTimeout(() => overlay.remove(), 200);
  }

  onunload() {
    this.close();
  }
};
