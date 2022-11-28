const Webpack = require('webpack');
const { merge } = require('webpack-merge');

const common = require('./webpack.common.js');

module.exports = merge(common, {
  mode: 'production',
  bail: true,
  output: {
    filename: 'js/[name].js',
    chunkFilename: 'js/[name].[chunkhash:8].chunk.js',
  },
  plugins: [
    new Webpack.DefinePlugin({
      'process.env.NODE_ENV': JSON.stringify('production'),
    }),
  ],
});
