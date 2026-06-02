"use strict";

Object.defineProperty(exports, "__esModule", { value: true });
exports.Extension = void 0;

const { getBuildHooks } = require("@diplodoc/cli");
const { getHooks: getMarkdownHooks } = require("@diplodoc/cli/lib/markdown");
const { getHooks: getLeadingHooks } = require("@diplodoc/cli/lib/leading");

class Extension {
    apply(program) {
        getBuildHooks(program).BeforeRun.for("html").tap("VcsPathFix", (run) => {
            let aliasesPrepared = false;

            const setVcsPath = (vfile) => {
                if (!aliasesPrepared) {
                    addPosixAliases(run.vcs.getData());
                    aliasesPrepared = true;
                }

                const path = normalizePath(vfile.path);
                const vcsPath = resolveVcsPath(run, path);

                console.log("[VcsPathFix]", path, "=>", vcsPath);

                run.meta.add(vfile.path, {
                    vcsPath,
                });

                return vfile;
            };

            getMarkdownHooks(run.markdown).Dump.tap(
                { name: "VcsPathFix", stage: -100 },
                setVcsPath,
            );

            getLeadingHooks(run.leading).Dump.tap(
                { name: "VcsPathFix", stage: -100 },
                setVcsPath,
            );
        });
    }
}

exports.Extension = Extension;

function normalizePath(path) {
    return String(path).replace(/\\/g, "/");
}

function addPosixAliases(data) {
    addMapAliases(data.mtimes);
    addMapAliases(data.authors);
    addMapAliases(data.contributors);
}

function addMapAliases(map) {
    if (!map) {
        return;
    }

    for (const [key, value] of Object.entries(map)) {
        const normalizedKey = normalizePath(key);

        if (normalizedKey !== key && !Object.prototype.hasOwnProperty.call(map, normalizedKey)) {
            map[normalizedKey] = value;
        }
    }
}

function resolveVcsPath(run, path) {
    const data = run.vcs.getData();

    const candidates = unique([
        path,
        path.replace(/^docs\//, ""),
        path.startsWith("docs/") ? path : `docs/${path}`,
    ]);

    for (const candidate of candidates) {
        if (hasVcsData(data, candidate)) {
            return candidate;
        }
    }

    return path.replace(/^docs\//, "");
}

function hasVcsData(data, path) {
    return Boolean(
        Object.prototype.hasOwnProperty.call(data.mtimes || {}, path) ||
        Object.prototype.hasOwnProperty.call(data.authors || {}, path) ||
        Object.prototype.hasOwnProperty.call(data.contributors || {}, path),
    );
}

function unique(items) {
    return Array.from(new Set(items));
}