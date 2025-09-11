const path = require('path');

module.exports = {
  entry: './src/index.ts',
  module: {
    rules: [
      {
        test: /\.ts$/,
        use: 'ts-loader',
        exclude: /node_modules/,
      },
    ],
  },
  resolve: {
    extensions: ['.ts', '.js'],
  },
  output: {
    filename: 'rum-bundle.js',
    path: path.resolve(__dirname, 'dist'),
    library: 'RUM',
    libraryTarget: 'umd',
    globalObject: 'this',
  },
  mode: 'production'
};