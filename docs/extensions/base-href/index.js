"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.Extension = void 0;
const { readFile, writeFile } = require("node:fs/promises");
const { join } = require("node:path");
const { getBuildHooks } = require("@diplodoc/cli");

class Extension {
    apply(program) {
        getBuildHooks(program).AfterRun.for("html").tapPromise("BaseHref", async (run) => {
            const file = join(run.output, "404.html");
            try {
                const html = await readFile(file, "utf8");
                await writeFile(file, html.replace(/<base href="[^"]*"/, '<base href="/"'));
            } catch (error) {
                run.logger.warn("BaseHref: unable to patch 404.html", error);
            }
        });
    }
}
exports.Extension = Extension;
