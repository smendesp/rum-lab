const { build } = require("esbuild");
const { dependencies, peerDependencies } = require('./package.json');

const sharedConfig = {
    entryPoints: ["src/rum.ts"],
    bundle: true,
    minify: false,
    // only needed if you have dependencies
    // external: Object.keys(dependencies).concat(Object.keys(peerDependencies)),
};

build({
    ...sharedConfig,
    platform: 'browser',
    format: 'esm',
    outfile: "dist/rum.js",
});