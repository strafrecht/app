const Webpack = require('webpack');
const { merge } = require('webpack-merge');
const Path = require('path');
const StylelintPlugin = require('stylelint-webpack-plugin');
const ESLintPlugin = require('eslint-webpack-plugin');

const common = require('./webpack.common.js');

module.exports = merge(common, {
  mode: 'development',
  devtool: 'inline-cheap-source-map',
  output: {
    chunkFilename: 'js/[name].chunk.js',
  },
  devServer: {
    hot: true,
    liveReload: true,
    open: true,
    port: 8080,
    static: {
      directory: require('path').join(__dirname, '../build'),
    },
  },
  plugins: [
    new Webpack.DefinePlugin({
      'process.env.NODE_ENV': JSON.stringify('development'),
    }),
    // Temporarily disabled for development - uncomment to enable linting
    // new ESLintPlugin({
    //   extensions: ['js', 'vue'],
    //   files: 'src',
    // }),
    // new StylelintPlugin({
    //   files: Path.join('src', '**/*.s?(a|c)ss'),
    // }),
  ],
});
