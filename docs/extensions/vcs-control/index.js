"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.Extension = void 0;
const node_assert_1 = require("node:assert");
const program_1 = require("@diplodoc/cli/lib/program");
const cli_1 = require("@diplodoc/cli");
const vcsTypeSet = new Set(['github', 'arcanum', 'custom']);
const urlPathVariable = '{path}';
class Extension {
    apply(program) {
        (0, program_1.getHooks)(program).Config.tap('VcsControl', (config) => {
            if (!config.vcsControl) {
                return config;
            }
            (0, node_assert_1.ok)("object" === typeof config.vcsControl, 'vcsControl must be object');
            (0, node_assert_1.ok)("url" in config.vcsControl, 'vcsControl.url must be required');
            (0, node_assert_1.ok)("string" === typeof config.vcsControl.url, 'vcsControl.url must be not empty');
            (0, node_assert_1.ok)(config.vcsControl.url.includes(urlPathVariable), `vcsControl.url not contains template variable ${urlPathVariable}`);
            (0, node_assert_1.ok)(vcsTypeSet.has(config.vcsControl.type), `vcsControl.type must be one of ${Array.from(vcsTypeSet).join(', ')}`);
            return config;
        });
        (0, cli_1.getBuildHooks)(program).BeforeRun.for('html').tapPromise('VcsControl', async (run) => {
            (0, cli_1.getEntryHooks)(run.entry).State.tap('VcsControl', (state) => {
                if (!program.config.vcsControl) {
                    return state;
                }
                const vcsControlConfig = program.config.vcsControl;
                state.data.vcsUrl = vcsControlConfig.url.replace(urlPathVariable, `${state.router.pathname}.md`);
                state.data.vcsType = vcsControlConfig.type;
                if (vcsControlConfig.icon) {
                    state.data.vcsIcon = vcsControlConfig.icon;
                }
                if (vcsControlConfig.hint) {
                    state.data.vcsHint = vcsControlConfig.hint;
                }
                return state;
            });
        });
    }
}
exports.Extension = Extension;
