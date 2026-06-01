"use strict";

const generatedIndentPattern = /\n {8}/g;

function fixCodeBlocks() {
  const codeBlocks = document.querySelectorAll("pre code");

  for (const codeBlock of codeBlocks) {
    const textNodes = document.createTreeWalker(codeBlock, NodeFilter.SHOW_TEXT);

    while (textNodes.nextNode()) {
      const textNode = textNodes.currentNode;
      const fixedText = textNode.textContent.replace(generatedIndentPattern, "\n");

      if (fixedText !== textNode.textContent) {
        textNode.textContent = fixedText;
      }
    }
  }
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", fixCodeBlocks, { once: true });
} else {
  fixCodeBlocks();
}
